from PyQt5 import QtWidgets
import abc


class AbstractSource(abc.ABC):
    def __init__(self, ui, data_handler):
        self.ui = ui
        self.filenames = []
        self.data_handler = data_handler

    @abc.abstractmethod
    def load_files(self, folder_path):
        raise NotImplementedError("Not implemented")

    def select_view(self):
        self.ui.fileSelector.clear()
        for file in self.filenames:
            self.ui.fileSelector.addItem(file)
        self.select_file()

    def select_file(self):
        self.load_analog_channels_ids()

        self.plot_info_view()
        self.plot_multiple_view()
        self.plot_list_view()

    def load_analog_channels_ids(self):
        path = self.ui.fileSelector.currentText()
        if path is None or len(path) == 0:
            return

        data_source = self.data_handler(path)
        channel_ids = data_source.get_analog_channels_ids()
        self.ui.channelSelector.clear()
        self.ui.channelSelector2.clear()
        for ch_id in channel_ids:
            self.ui.channelSelector.addItem(str(ch_id))
            self.ui.channelSelector2.addItem(str(ch_id))
        self.ui.recording_start_s = 0

    def plot_info_view(self):
        path = self.ui.fileSelector.currentText()
        if not path:
            return
        data_source = self.data_handler(path)
        info = data_source.get_info()

        row = 0
        self.ui.infoTable.setRowCount(len(info))
        for key, value in info.items():
            key_item = QtWidgets.QTableWidgetItem(key)
            value_item = QtWidgets.QTableWidgetItem(value)

            self.ui.infoTable.setItem(row, 0, key_item)
            self.ui.infoTable.setItem(row, 1, value_item)

            row += 1
        self.ui.infoTable.setHorizontalHeaderLabels(["Key", "Value"])
        self.ui.infoTable.resizeColumnsToContents()

    def plot_single_view(self):
        path = self.ui.fileSelector.currentText()
        channel_id = self.ui.channelSelector.currentText()
        if self.ui.is_single_view_selected() and path and channel_id:
            self._plot_single_view(path, int(channel_id))
            self.ui.update()

    @abc.abstractmethod
    def _plot_single_view(self, path, channel_id):
        raise NotImplementedError('Not implemented')

    def plot_multiple_view(self):
        path = self.ui.fileSelector.currentText()
        if self.ui.is_grid_view_selected() and path:
            self._plot_grid_view(path)
            self.ui.update()

    @abc.abstractmethod
    def _plot_grid_view(self, path):
        raise NotImplementedError('Not implemented')

    def plot_list_view(self):
        channel_id = self.ui.channelSelector.currentText()
        if self.ui.is_list_view_selected() and channel_id:
            self._plot_list_view(int(channel_id))
            self.ui.update()

    @abc.abstractmethod
    def _plot_list_view(self, channel_id):
        raise NotImplementedError('Not implemented')

