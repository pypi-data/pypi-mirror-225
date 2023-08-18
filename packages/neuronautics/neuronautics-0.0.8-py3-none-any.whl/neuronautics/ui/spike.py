import glob

import numpy as np

from ..recordings.nn_spike import NNSpike

from ..mlkit.spike_sorter import SpikeSorter

from ..utils.logger import Logger
from ..ui.abstract_source import AbstractSource

SINGLE_VIEW_LENGTH_S = 5
GRID_VIEW_STACKED_S = 30
GRID_VIEW_TIMESERIES_S = 0.3

logger = Logger.get_logger()


class Spike(AbstractSource):
    """
    A class representing spike data visualization and processing.

    This class handles the visualization and processing of spike data, including
    loading files, plotting different views, running k-means clustering, saving data,
    and managing signal unit changes.

    Methods:
        __init__(self, ui): Constructor to initialize the Spike object.
        load_files(self, folder_path): Load spike files from the given folder path.
        select_view(self): Select and display the spike view.
        _plot_single_view(self, path, channel_id): Plot single view of spike data.
        _plot_grid_view(self, path): Plot grid view of spike data.
        _plot_list_view(self, channel_id): Plot list view of spike data.
        all_data(self): Get all spike data.
        run_kmeans(self): Perform k-means clustering on spike data.
        run_all_kmeans(self): Perform k-means clustering on all spike data channels.
        reset_spike_classes(self): Reset spike classes to default.
        signal_unit_changed(self, changes): Update spike unit classes based on changes.
        save_spikes(self): Save spike data.
    """
    def __init__(self, ui):
        super().__init__(ui, NNSpike)

    def load_files(self, folder_path):
        """
        Load spike files from the given folder path.

        Args:
            folder_path (str): Path to the folder containing spike files.
        """
        self.ui.spikeBtn.setEnabled(False)

        self.filenames = sorted(glob.glob(f"{folder_path}/*.spike"))

        if len(self.filenames) > 0:
            self.ui.spikeBtn.setEnabled(True)

    def select_view(self):
        """
        Selects and displays the spike view.

        This method is called to select the spike view and update the user interface
        accordingly. It sets the current widget of the option stack to the spike
        options page.

        Usage:
            Call this method when you want to switch to the spike view.
        """
        super().select_view()
        self.ui.optionStck.setCurrentWidget(self.ui.spikeOptPage)

    def _plot_single_view(self, path, channel_id):
        as_timeseries = 1-int(self.ui.chkSpikeStacked.isChecked())
        nn = self.data_handler(path)
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
            .plot(values=values, group=group, allow_selection=True,
                  xlim=xlim, progress_bar=True)
        )

    def _plot_grid_view(self, path):
        nn = self.data_handler(path)
        as_timeseries = 1-int(self.ui.chkSpikeStacked.isChecked())

        start_ms = int(self.ui.recording_start_s) * 1_000

        if as_timeseries == 1:
            end_ms = int((self.ui.recording_start_s + GRID_VIEW_TIMESERIES_S) * 1_000)
            xlim = (start_ms-1, end_ms)
        else:
            end_ms = int((self.ui.recording_start_s + GRID_VIEW_STACKED_S) * 1_000)
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
            end_ms = int((self.ui.recording_start_s + GRID_VIEW_TIMESERIES_S) * 1_000)
            xlim = (start_ms-1, end_ms)
        else:
            end_ms = int((self.ui.recording_start_s + GRID_VIEW_STACKED_S) * 1_000)
            xlim = None

        channel_values = dict()
        for ix, fn in enumerate(self.filenames):

            logger.log_process('_plot_list_view', ix, len(self.filenames))
            name = fn.split('/')[-1].replace('.spike', '')
            nn = self.data_handler(fn)

            channel_data = nn.get_channel_data(channel_id, start_ms, end_ms)

            values, group = [], []
            for ix, (cl, t, spk) in channel_data.iterrows():
                values.append([(t * as_timeseries + nn.to_ms(x, 'tick') - 1, y) for x, y in enumerate(spk)])
                group.append(cl)
            channel_values[name] = (values, group)

        logger.log_process('_plot_list_view', len(self.filenames), len(self.filenames))

        self.ui.list_chart_view.plot(channel_values, xlim=xlim)

    def all_data(self):
        """
        Retrieves all spike data from the currently selected file.

        This method retrieves all spike data from the currently selected file
        using the NNSpike class and returns it as a DataFrame.

        Returns:
            pandas.DataFrame: A DataFrame containing all spike data.

        Usage:
            spike_instance = Spike(ui)
            data_frame = spike_instance.all_data()
        """
        path = self.ui.fileSelector.currentText()
        nn = self.data_handler(path)
        df = nn.get_all_data(0, np.Inf)
        return df

    def all_channel_data(self):
        """
        Retrieves all spike data from the currently selected file and channel.

        This method retrieves all spike data from the currently selected file and channel
        using the NNSpike class and returns it as a DataFrame.

        Returns:
            pandas.DataFrame: A DataFrame containing all spike data.

        Usage:
            spike_instance = Spike(ui)
            data_frame = spike_instance.all_channel_data()
        """
        path = self.ui.fileSelector.currentText()
        channel_id = int(self.ui.channelSelector.currentText())
        nn = self.data_handler(path)
        df = nn.get_channel_data(channel_id, 0, np.Inf)
        return df

    def run_kmeans(self):
        """
        Runs k-means clustering on spike data for the current channel.

        This method performs k-means clustering on the spike data for the current
        channel using the specified number of principal components and clusters.
        It then sets the computed labels for the channel using the NNSpike class.

        Usage:
            spike_instance = Spike(ui)
            spike_instance.run_kmeans()

        Notes:
            This method requires a valid file selection and channel choice in the UI.
        """
        path, channel_id, num_pca, num_clusters = self._get_kmeans_params()

        df = self.all_channel_data()
        labels = self._pca_kmeans(df, num_pca, num_clusters)

        nn = self.data_handler(path)
        nn.set_labels(channel_id, labels)

        self.plot_single_view()

    def _get_kmeans_params(self):
        path = self.ui.fileSelector.currentText()
        channel_id = int(self.ui.channelSelector.currentText())
        num_pca = self.ui.pcaValue.value()
        num_clusters = self.ui.kValue.value()
        return path, channel_id, num_pca, num_clusters

    def _pca_kmeans(self, df, num_pca, num_clusters):
        # Extract spike data for the current channel
        spike_data = np.array(df['spike'].tolist())
        labels = (
            SpikeSorter(spike_data)
            .pca(num_pca)
            .kmeans(num_clusters)
            .run()
        )
        return labels

    def run_all_kmeans(self):
        """
        Runs k-means clustering on spike data for all channels.

        This method performs k-means clustering on the spike data for all channels
        using the specified number of principal components and clusters. It iterates
        through each channel, computes labels, and sets them using the NNSpike class.

        Usage:
            spike_instance = Spike(ui)
            spike_instance.run_all_kmeans()

        Notes:
            This method requires a valid file selection.
        """
        path, _, num_pca, num_clusters = self._get_kmeans_params()

        nn = self.data_handler(path)
        df = nn.get_all_data(0, np.Inf)

        logger = Logger.get_logger()

        grouped = df.groupby('channel_id')
        n_groups = len(grouped)
        logger.log_process('run_all_kmeans', 0, n_groups)
        for ix, (channel_id, group) in enumerate(grouped):
            logger.log_process('run_all_kmeans', ix, n_groups)
            labels = self._pca_kmeans(group, num_pca, num_clusters)
            nn.set_labels(channel_id, labels)

        logger.log_process('run_all_kmeans', n_groups, n_groups)

        self.plot_single_view()
        self.plot_multiple_view()

    def reset_spike_classes(self):
        """
        Resets spike classes to the default value for the current channel.

        This method resets the spike classes for the current channel to the default
        value (0) using the NNSpike class. It effectively clears any clustering
        labels that were previously applied.

        Usage:
            spike_instance = Spike(ui)
            spike_instance.reset_spike_classes()

        Notes:
            This method requires a valid file selection and channel choice in the UI.
        """
        path, channel_id, _, _ = self._get_kmeans_params()

        nn = self.data_handler(path)
        df = nn.get_channel_data(channel_id, 0, np.Inf)

        nn.set_labels(channel_id, [0] * len(df))

        self.plot_single_view()

    def signal_unit_changed(self, changes):
        """
        Update spike unit classes based on changes.

        This method updates the spike unit classes based on the provided changes
        using the NNSpike class. It merges the changes with the existing spike data
        and updates the labels accordingly.

        Args:
            changes (list of tuples): A list of tuples containing timestamp (in ms)
                                      and new unit class values.

        Usage:
            spike_instance = Spike(ui)
            changes = [(timestamp_1, new_class_1), (timestamp_2, new_class_2)]
            spike_instance.signal_unit_changed(changes)

        Notes:
            This method requires a valid file selection and channel choice in the UI.
        """
        path, channel_id, _, _ = self._get_kmeans_params()

        nn = self.data_handler(path)
        df = nn.get_channel_data(channel_id, 0, np.Inf)

        import pandas as pd
        changes_df = pd.DataFrame(changes, columns=['ts_ms', 'new_class'])
        merged_df = pd.merge(df, changes_df, on='ts_ms', how='left')
        merged_df['class'] = merged_df['new_class'].combine_first(merged_df['class'])

        nn.set_labels(channel_id, list(merged_df['class']))

    def save_spikes(self):
        """
        Save spike data to the original file.

        This method saves the modified spike data to the original file using the
        NNSpike class. It ensures that any changes made to the spike data, such as
        clustering labels, are persisted in the file.

        Usage:
            spike_instance = Spike(ui)
            spike_instance.save_spikes()

        Notes:
            This method requires a valid file selection.
        """
        path = self.ui.fileSelector.currentText()
        self.data_handler(path).save()
