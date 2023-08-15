from PyQt5 import QtWidgets
import glob

import numpy as np

from neuronautics.recordings.mcs_raw import McsRaw
from neuronautics.ui.abstract_source import AbstractSource

from neuronautics.utils.logger import Logger

SINGLE_VIEW_LENGTH_S = 5
GRID_VIEW_LENGTH_S = 0.3


class Raw(AbstractSource):
    def __init__(self, ui):
        super().__init__(ui, McsRaw)

    def load_files(self, folder_path):
        self.ui.rawBtn.setEnabled(False)

        self.filenames = sorted(glob.glob(f"{folder_path}/*.h5"))

        fns = [self.get_filename(path) for path in self.filenames]
        self.ui.list_chart_view.setup_grid(nrows=int(np.ceil(len(self.filenames)/2)), ncols=2, plot_names=fns
                                           , show_axis=True)

        if len(self.filenames) > 0:
            self.ui.rawBtn.setEnabled(True)

    def select_view(self):
        super().select_view()
        self.ui.optionStck.setCurrentWidget(self.ui.rawOptPage)

    def _plot_single_view(self, path, channel_id):
        channel_id = int(channel_id)
        mcs = McsRaw(path)

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
        mcs = McsRaw(path)
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
            mcs = McsRaw(path)
            start_idx = mcs.to_ticks(self.ui.recording_start_s, 'second')
            end_idx = mcs.to_ticks(self.ui.recording_start_s + GRID_VIEW_LENGTH_S, 'second')
            channel_data = mcs.get_channel_data(channel_id, start_idx, end_idx)
            data[self.get_filename(path)] = channel_data
        (
            self.ui.list_chart_view
            .plot_xy(data)
        )

    def get_filename(self, path):
        return path.split('/')[-1].replace('.h5', '')

    def extract_spikes(self):
        path = self.ui.fileSelector.currentText()
        sigma = self.ui.sigmaValue.value()
        window_ms = self.ui.windowValue.value()
        if path:
            mcs = McsRaw(path)
            spikes = mcs.extract_all_spikes(sigma, window_ms)
            spikes.to_csv(path.replace('h5', 'spike'), index=False)

    def extract_all_spikes(self):
        num_items = self.ui.fileSelector.count()
        for i in range(num_items):
            self.ui.fileSelector.setCurrentIndex(i)
            self.ui.update()
            QtWidgets.QApplication.processEvents()
            self.extract_spikes()

