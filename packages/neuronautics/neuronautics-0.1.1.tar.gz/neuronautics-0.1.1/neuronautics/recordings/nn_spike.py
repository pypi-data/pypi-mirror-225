from neuronautics.recordings.abstract_spike import AbstractSpike

import pandas as pd
from neuronautics.utils.helpers import convert_to_array
from functools import lru_cache

@lru_cache()
def fetch_spikes(filename):
    print('Fetching spikes')
    data = pd.read_csv(filename)
    data['channel_id'] = data.channel_id.astype(int)
    data['spike'] = data['spike'].apply(convert_to_array)
    return data


class NNSpike(AbstractSpike):

    def __init__(self, filename):
        self.filename = filename
        self.data = fetch_spikes(filename)

    def get_info(self):
        return {'N. channels': len(self.get_analog_channels_ids())}

    def get_analog_channels_ids(self):
        return sorted(list(self.data.channel_id.astype(int).drop_duplicates()))

    def get_channel_data(self, channel_id, from_ms, to_ms):
        channel_data = self.data[self.data.channel_id == channel_id]
        channel_data = channel_data[(from_ms<=channel_data.ts_ms) & (channel_data.ts_ms<to_ms)]
        return channel_data[['class', 'ts_ms', 'spike']]

    def get_all_data(self, from_ms, to_ms):
        channel_data = self.data
        channel_data = channel_data[(from_ms<=channel_data.ts_ms) & (channel_data.ts_ms<to_ms)]
        return channel_data[['channel_id', 'class', 'ts_ms', 'spike']]

    def set_labels(self, channel_id, labels):
        self.data.loc[self.data['channel_id'] == channel_id, 'class'] = labels

    def save(self):
        self.data.to_csv(self.filename, index=False)

    def to_ms(self, data, units):
        factors = { 'tick': 0.1 }
        return data*factors[str(units)]
