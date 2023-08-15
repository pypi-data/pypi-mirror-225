import McsPy.McsData
import McsPy.McsCMOS

from neuronautics.recordings.abstract_raw import AbstractRaw
from neuronautics.recordings.config import MAX_WORKERS

import numpy as np
import pandas as pd
import concurrent.futures
import os

from neuronautics.utils.logger import Logger
from neuronautics.utils.helpers import convert_to_array
from functools import lru_cache


TMP_FILE = '/tmp/spikes.csv'
TMP_PARTIAL_FILE = lambda fid: f'/tmp/spikes_{fid}.csv'


@lru_cache()
def fetch_raw(filename):
    return McsPy.McsData.RawData(filename)


def parallel_extract_spike(filename, ch_id, sigma, window_ms):
    spikes = McsRaw(filename).extract_spike(ch_id, sigma, window_ms)
    filename = TMP_PARTIAL_FILE(ch_id)
    spikes.to_csv(filename, index=False)
    return filename


def parallel_get_data(filename, ch_id, from_ix, to_ix):
    return ch_id, McsRaw(filename).get_channel_data(ch_id, from_ix, to_ix)


class McsRaw(AbstractRaw):
    logger = Logger.get_logger()

    def __init__(self, filename):
        self.filename = filename
        self.data = fetch_raw(filename)

    def __getstate__(self):
        return {'filename': self.filename}

    def __setstate__(self, state):
        self.filename = state['filename']
        self.data = fetch_raw(self.filename)

    @classmethod
    def _get_recording_info(cls, rec_id, rec) -> dict:
        recording_time = 0
        recording_unit = ''
        units = ['h', 'min', 's', 'ms']
        for unit in units:
            recording_time = rec.duration_time.m_as(unit)
            recording_unit = unit
            if recording_time > 1:
                break

        return {
            f'[{rec_id}] recording time': f'{recording_time:.2f} {recording_unit}',
        }

    def _get_recording(self, recording_id=None):
        recording_id = list(self.data.recordings.keys())[0] if recording_id is None else recording_id
        return self.data.recordings[recording_id]

    def _get_analog_stream(self, analog_stream_id=None):
        analog_stream_id = list(self._get_recording().analog_streams.keys())[0] if analog_stream_id is None \
                                                                                else analog_stream_id
        return self._get_recording().analog_streams[analog_stream_id]

    def get_analog_channels_ids(self):
        return list(self._get_analog_stream().channel_infos.keys())

    def get_info(self):
        data = self.data
        info = {
            'MEA Layout': data.mea_layout,
            'recording date': str(data.date),
            'comment': data.comment,
            'recordings ids': ', '.join([str(k) for k in data.recordings.keys()]),
        }
        for k in data.recordings.keys():
            info = {**info, **self._get_recording_info(k, data.recordings[k])}

        return info

    @classmethod
    def _to_microvolts(cls, data, units):
        factors = {'volt': 1_000_000}
        return data*factors[str(units)]

    def to_seconds(self, data, units):
        factors = {'microsecond': 1/1_000_000,
                   'millisecond': 1/1_000,
                   'second'     : 1,
                   'minute'     : 60,
                   'hour'       : 3600,
                   'tick'       : self._get_analog_stream().channel_infos[0].sampling_tick.m_as('millisecond')/1_000}
        return data*factors[str(units)]

    def to_ticks(self, data, units):
        data = self.to_seconds(data, units)
        tick = self._get_analog_stream().channel_infos[0].sampling_tick.m_as('second')
        return int(data / tick)

    def get_channel_data(self, channel_id, from_ix, to_ix):
        series, unit_v = self._get_analog_stream().get_channel_in_range(channel_id, from_ix, to_ix)
        time, unit_t = self._get_analog_stream().get_channel_sample_timestamps(0, from_ix, to_ix)
        series = self._to_microvolts(series, unit_v)
        time = self.to_seconds(time, unit_t)
        return time, series

    def get_all_data(self, from_ix, to_ix):
        channel_data = {}
        with concurrent.futures.ProcessPoolExecutor(max_workers=MAX_WORKERS) as executor:
            futures = [executor.submit(parallel_get_data,
                                       self.filename, ch_id, from_ix, to_ix)
                       for ch_id in self.get_analog_channels_ids()]
            for future in concurrent.futures.as_completed(futures):
                ch_id, spikes = future.result()
                channel_data[ch_id] = spikes
        return channel_data

    def extract_spike(self, channel_id, sigma, window_ms, pre_spike_ms=1, pos_spike_ms=2):
        try:
            window_ticks = self.to_ticks(window_ms, 'millisecond')
            pre_spike_ticks = self.to_ticks(pre_spike_ms, 'millisecond')
            pos_spike_ticks = self.to_ticks(pos_spike_ms, 'millisecond')
            channel_data, unit_v = self._get_analog_stream().get_channel_in_range(channel_id, 0, self._get_recording().duration)
            channel_data = self._to_microvolts(channel_data, unit_v)
            if window_ms == 0:
                ma = channel_data.mean()
                ms = channel_data.std()
                mask = np.abs(channel_data) > (ma + sigma*ms)
            else:
                from neuronautics.utils.helpers import moving_average
                ma, ms = moving_average(channel_data, window_ticks)
                mask = np.abs(channel_data[-len(ma):]) > (ma + sigma*ms)
            indexes = np.where(mask)[0]

            aux_index = 0
            spikes = list()
            for index in indexes:
                if index > aux_index and (index < len(channel_data)-window_ticks):
                    rel_pos = window_ticks+index
                    shift = np.abs(channel_data[rel_pos:rel_pos+pre_spike_ticks]).argmax()
                    rel_pos = rel_pos + shift
                    shift_index = index + shift
                    aux_index = index + shift + pre_spike_ticks + 1
                    spike = channel_data[rel_pos-pre_spike_ticks:rel_pos+pos_spike_ticks]

                    if ms[index] > 0 and len(spike) == (pre_spike_ticks + pos_spike_ticks):
                        spikes.append((channel_id, rel_pos, self.to_seconds(rel_pos, 'tick') * 1_000
                                       , 0, ma[shift_index], ms[shift_index]
                                       , (abs(spike[pre_spike_ticks])-ma[shift_index]) / ms[shift_index], spike))

            spikes = pd.DataFrame(spikes, columns=['channel_id', 'tick', 'ts_ms', 'class', 'avg', 'std', 'sigma', 'spike'])

        except:
            print(f'>>> Channel {channel_id} failed at {index}')
            spikes = pd.DataFrame(spikes, columns=['channel_id', 'tick', 'ts_ms', 'class', 'avg', 'std', 'sigma', 'spike'])

        return spikes

    def extract_all_spikes(self, sigma, window_ms, pre_spike_ms=1, pos_spike_ms=2):
        spikes_files = []
        i = 1
        self.logger.log_process('extract_spike', 0, len(self.get_analog_channels_ids()))
        with concurrent.futures.ProcessPoolExecutor(max_workers=MAX_WORKERS) as executor:
            futures = [executor.submit(parallel_extract_spike,
                                       self.filename, ch_id, sigma, window_ms, pre_spike_ms, pos_spike_ms)
                       for ch_id in self.get_analog_channels_ids()]
            for future in concurrent.futures.as_completed(futures):
                spikes_files.append(future.result())
                self.logger.log_process('extract_spike', i, len(self.get_analog_channels_ids()))
                i += 1

        # Merge individual CSV files into a single CSV file
        with open(TMP_FILE, 'w') as outfile:
            for ix, filename in enumerate(spikes_files):
                with open(filename) as infile:
                    if ix==0:
                        lines = infile.readlines()
                    else:
                        lines = infile.readlines()[1:]
                    outfile.write("\n".join(lines))

        # Remove the individual CSV files
        for filename in spikes_files:
            os.remove(filename)

        # Read the merged CSV file into a DataFrame
        spikes = pd.read_csv(TMP_FILE)

        # Apply the convert_to_array function to the 'spike' column
        spikes['spike'] = spikes['spike'].apply(convert_to_array)
        return spikes

