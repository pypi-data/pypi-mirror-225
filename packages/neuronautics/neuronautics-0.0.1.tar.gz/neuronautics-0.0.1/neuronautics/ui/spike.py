import glob

import numpy as np

from neuronautics.recordings.nn_spike import NNSpike

from neuronautics.mlkit.spike_sorter import SpikeSorter

from neuronautics.utils.logger import Logger
from neuronautics.ui.abstract_source import AbstractSource

SINGLE_VIEW_LENGTH_S = 5
GRID_VIEW_STACKED_S = 30
GRID_VIEW_TIMESERIES_S = 0.3

logger = Logger.get_logger()


class Spike(AbstractSource):
    def __init__(self, ui):
        super().__init__(ui, NNSpike)

    def load_files(self, folder_path):
        self.ui.spikeBtn.setEnabled(False)

        self.filenames = sorted(glob.glob(f"{folder_path}/*.spike"))

        if len(self.filenames) > 0:
            self.ui.spikeBtn.setEnabled(True)

    def select_view(self):
        super().select_view()
        self.ui.optionStck.setCurrentWidget(self.ui.spikeOptPage)

    def _plot_single_view(self, path, channel_id):
        as_timeseries = 1-int(self.ui.chkSpikeStacked.isChecked())
        nn = NNSpike(path)
        start_ms = int(self.ui.recording_start_s) * 1_000
        if as_timeseries == 1:
            end_ms = int(self.ui.recording_start_s + SINGLE_VIEW_LENGTH_S) * 1_000
            xlim = (start_ms-1, end_ms)
        else:
            end_ms = np.Inf
            xlim = None
        channel_data = nn.get_channel_data(channel_id, start_ms, end_ms)

        values, group = [], []
        for ix, (cl, t, spk) in channel_data.iterrows():
            values.append([(t * as_timeseries + nn.to_ms(x, 'tick') - 1, y) for x, y in enumerate(spk)])
            group.append(cl)

        (
            self.ui.single_chart_view
            .x_label('Time (ms)')
            .y_label('Microvolts')
            .title(f'Channel {channel_id}')
            .plot(values=values, group=group, allow_selection=True, xlim=xlim, progress_bar=True)
        )

    def _plot_grid_view(self, path):
        nn = NNSpike(path)
        as_timeseries = 1-int(self.ui.chkSpikeStacked.isChecked())

        start_ms = int(self.ui.recording_start_s) * 1_000

        if as_timeseries == 1:
            end_ms = int(self.ui.recording_start_s + GRID_VIEW_TIMESERIES_S) * 1_000
            xlim = (start_ms-1, end_ms)
        else:
            end_ms = int(self.ui.recording_start_s + GRID_VIEW_STACKED_S) * 1_000
            xlim = None

        channel_data = nn.get_all_data( start_ms, end_ms)

        channel_values = dict()
        for ix, (ch_id, cl, t, spk) in channel_data.iterrows():
            values, group = channel_values.get(ch_id, ([], []))
            values.append([(t * as_timeseries + nn.to_ms(x, 'tick') - 1, y) for x, y in enumerate(spk)])
            group.append(cl)
            channel_values[ch_id] = (values, group)

        (
            self.ui.multiple_chart_view
            .plot(channel_values, xlim=xlim)
        )

    def _plot_list_view(self, channel_id):
        as_timeseries = 1-int(self.ui.chkSpikeStacked.isChecked())
        start_ms = int(self.ui.recording_start_s) * 1_000

        if as_timeseries == 1:
            end_ms = int(self.ui.recording_start_s + GRID_VIEW_TIMESERIES_S) * 1_000
            xlim = (start_ms-1, end_ms)
        else:
            end_ms = int(self.ui.recording_start_s + GRID_VIEW_STACKED_S) * 1_000
            xlim = None

        channel_values = dict()
        for ix, fn in enumerate(self.filenames):

            logger.log_process('_plot_list_view', ix, len(self.filenames))
            name = fn.split('/')[-1].replace('.spike', '')
            nn = NNSpike(fn)

            channel_data = nn.get_channel_data(channel_id, start_ms, end_ms)

            values, group = [], []
            for ix, (cl, t, spk) in channel_data.iterrows():
                values.append([(t * as_timeseries + nn.to_ms(x, 'tick') - 1, y) for x, y in enumerate(spk)])
                group.append(cl)
            channel_values[name] = (values, group)

        logger.log_process('_plot_list_view', len(self.filenames), len(self.filenames))

        self.ui.list_chart_view.plot(channel_values, xlim=xlim)

    def all_data(self):
        path = self.ui.fileSelector.currentText()
        nn = NNSpike(path)
        df = nn.get_all_data(0, np.Inf)
        return df

    def run_kmeans(self):
        path = self.ui.fileSelector.currentText()
        channel_id = int(self.ui.channelSelector.currentText())
        num_pca = self.ui.pcaValue.value()
        num_clusters = self.ui.kValue.value()

        nn = NNSpike(path)
        df = nn.get_channel_data(channel_id, 0, np.Inf)

        # Extract spike data for the current channel
        spike_data = np.array(df['spike'].tolist())

        labels = (
            SpikeSorter(spike_data)
            .pca(num_pca)
            .kmeans(num_clusters)
            .run()
        )

        nn.set_labels(channel_id, labels)

        self.plot_single_view()

    def run_all_kmeans(self):
        path = self.ui.fileSelector.currentText()
        num_pca = self.ui.pcaValue.value()
        num_clusters = self.ui.kValue.value()

        nn = NNSpike(path)
        df = nn.get_all_data(0, np.Inf)

        logger = Logger.get_logger()

        grouped = df.groupby('channel_id')
        n_groups = len(grouped)
        logger.log_process('run_all_kmeans', 0, n_groups)
        for ix, (channel_id, group) in enumerate(grouped):
            logger.log_process('run_all_kmeans', ix, n_groups)
            spike_data = np.array(group['spike'].tolist())

            labels = (
                SpikeSorter(spike_data)
                .pca(num_pca)
                .kmeans(num_clusters)
                .run()
            )

            nn.set_labels(channel_id, labels)

        logger.log_process('run_all_kmeans', n_groups, n_groups)

        self.plot_single_view()
        self.plot_multiple_view()

    def reset_spike_classes(self):
        path = self.ui.fileSelector.currentText()
        channel_id = int(self.ui.channelSelector.currentText())

        nn = NNSpike(path)
        df = nn.get_channel_data(channel_id, 0, np.Inf)

        nn.set_labels(channel_id, [0] * len(df))

        self.plot_single_view()

    def signal_unit_changed(self, changes):
        path = self.ui.fileSelector.currentText()
        channel_id = int(self.ui.channelSelector.currentText())
        nn = NNSpike(path)
        df = nn.get_channel_data(channel_id, 0, np.Inf)

        import pandas as pd
        changes_df = pd.DataFrame(changes, columns=['ts_ms', 'new_class'])
        merged_df = pd.merge(df, changes_df, on='ts_ms', how='left')
        merged_df['class'] = merged_df['new_class'].combine_first(merged_df['class'])

        nn.set_labels(channel_id, list(merged_df['class']))

    def save_spikes(self):
        path = self.ui.fileSelector.currentText()
        NNSpike(path).save()
