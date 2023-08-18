from PyQt5 import QtWidgets
import glob

import numpy as np

from ..recordings.mcs_raw import McsRaw
from ..ui.abstract_source import AbstractSource

from ..utils.logger import Logger

SINGLE_VIEW_LENGTH_S = 5
GRID_VIEW_LENGTH_S = 0.3


class Raw(AbstractSource):
    """
    A class for handling raw data visualization and spike extraction.

    This class handles the visualization and processing of raw data, including
    loading files, plotting different views and extracting spikes.

    Methods:
        __init__(self, ui): Initializes the Raw instance.
        load_files(self, folder_path): Loads file names from a folder.
        select_view(self): Selects the raw data view.
        _plot_single_view(self, path, channel_id): Plots a single channel view.
        _plot_grid_view(self, path): Plots a grid view of multiple channels.
        _plot_list_view(self, channel_id): Plots a list view of channels.
        get_filename(cls, path): Extracts the filename from a path.
        extract_spikes(self): Extracts spikes from the selected file.
        extract_all_spikes(self): Extracts spikes from all files.

    """
    def __init__(self, ui):
        super().__init__(ui, McsRaw)

    def load_files(self, folder_path):
        """
        Load spike files from the given folder path.

        Args:
            folder_path (str): Path to the folder containing h5 files.
        """
        self.ui.rawBtn.setEnabled(False)

        self.filenames = sorted(glob.glob(f"{folder_path}/*.h5"))

        fns = [self.get_filename(path) for path in self.filenames]
        self.ui.list_chart_view.setup_grid(nrows=int(np.ceil(len(self.filenames)/2)), ncols=2, plot_names=fns
                                           , show_axis=True)

        if len(self.filenames) > 0:
            self.ui.rawBtn.setEnabled(True)

    def select_view(self):
        """
        Selects and displays the raw view.

        This method is called to select the raw view and update the user interface
        accordingly. It sets the current widget of the option stack to the raw
        options page.

        Usage:
            Call this method when you want to switch to the raw view.
        """
        super().select_view()
        self.ui.optionStck.setCurrentWidget(self.ui.rawOptPage)

    def _plot_single_view(self, path, channel_id):
        channel_id = int(channel_id)
        mcs = self.data_handler(path)

        start_idx = mcs.to_ticks(self.ui.recording_start_s, 'second')
        end_idx = mcs.to_ticks(self.ui.recording_start_s + SINGLE_VIEW_LENGTH_S, 'second')
        time, series = mcs.get_channel_data(channel_id, start_idx, end_idx)
        (
            self.ui.single_chart_view
            .x_label('Time (seconds)')
            .y_label('Microvolts')
            .title(f'Channel {channel_id}')
            .plot_xy(time, series)
        )

    def _plot_grid_view(self, path):
        mcs = self.data_handler(path)
        start_idx = mcs.to_ticks(self.ui.recording_start_s, 'second')
        end_idx = mcs.to_ticks(self.ui.recording_start_s + GRID_VIEW_LENGTH_S, 'second')
        channel_data = mcs.get_all_data(start_idx, end_idx)
        (
            self.ui.multiple_chart_view
            .plot_xy(channel_data)
        )

    def _plot_list_view(self, channel_id):
        data = dict()
        for path in self.filenames:
            mcs = self.data_handler(path)
            start_idx = mcs.to_ticks(self.ui.recording_start_s, 'second')
            end_idx = mcs.to_ticks(self.ui.recording_start_s + GRID_VIEW_LENGTH_S, 'second')
            channel_data = mcs.get_channel_data(channel_id, start_idx, end_idx)
            data[self.get_filename(path)] = channel_data
        (
            self.ui.list_chart_view
            .plot_xy(data)
        )

    @classmethod
    def get_filename(cls, path):
        """
        Extracts the filename from the given path.

        Args:
            path: The full path to the file.

        Returns:
            str: The extracted filename.
        """
        return path.split('/')[-1].replace('.h5', '')

    def extract_spikes(self):
        """
        Extracts spike events from the selected data file and saves them to a spike file.

        This method extracts spike events from the currently selected data file, using the specified parameters for
        spike detection.

        The spike events are detected based on the given sigma and window values. A Gaussian filter with the specified
        sigma is applied to the raw data, and threshold crossings exceeding the specified window duration are
        considered as spike events.

        After extracting spike events, the resulting spike events are saved to a CSV file in the same directory as the
        data file. The filename for the spike file is derived from the original data file name by replacing the '.h5'
        extension with '.spike'.

        Note:
            - The data file must be selected in the UI's file selector before calling this method.
            - The sigma and window parameters are determined by the UI's corresponding user inputs.

        """
        path = self.ui.fileSelector.currentText()
        sigma = self.ui.sigmaValue.value()
        window_ms = self.ui.windowValue.value()
        if path:
            mcs = self.data_handler(path)
            spikes = mcs.extract_all_spikes(sigma, window_ms)
            spikes.to_csv(path.replace('h5', 'spike'), index=False)

    def extract_all_spikes(self):
        """
        Extracts spike events from all data files and saves them to individual spike files.

        This method iterates through all available data files in the file selector of the UI and extracts spike events
        from each file. Spike detection is performed using the specified parameters for spike detection, such as sigma
        and window duration.

        For each data file, spike events are detected based on the given parameters.

        After extracting spike events for each data file, the resulting spike events are saved to individual CSV files
        in the same directories as the corresponding data files. The filenames for the spike files are derived from the
        original data file names by replacing the '.h5' extension with '.spike'.

        Note:
            - The sigma and window parameters are determined by the UI's corresponding user inputs.

        """
        num_items = self.ui.fileSelector.count()
        for i in range(num_items):
            self.ui.fileSelector.setCurrentIndex(i)
            self.ui.update()
            QtWidgets.QApplication.processEvents()
            self.extract_spikes()

