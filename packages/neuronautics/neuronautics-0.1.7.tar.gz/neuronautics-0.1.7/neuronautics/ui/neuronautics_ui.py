import resource
# data handlers
from neuronautics.ui.raw import Raw
from neuronautics.ui.spike import Spike

from neuronautics.analysis.loader import Loader

# plotters
from neuronautics.plotters.line_2d import Line2D
from neuronautics.plotters.grid_line_2d import GridLine2D

# ui handlers
from neuronautics.ui.analysis_ui import AnalysisUi
from neuronautics.ui.layout_ui import LayoutUi

# logger
from neuronautics.utils.logger import Logger

# pyqt
from PyQt5 import QtWidgets, uic
from PyQt5.QtCore import QTimer, Qt
from PyQt5.QtWidgets import QMessageBox, QTreeWidgetItem

CLOCK_SPEED_MS = 10
RECORDING_STEP_S = 0.1


class NeuronauticsUi(QtWidgets.QMainWindow):
    def __init__(self):
        super(NeuronauticsUi, self).__init__()
        uic.loadUi('ui/neuronautics.ui', self)
        self.single_chart_view = Line2D(self.singleChart)
        self.single_chart_view.signal_unit_changed.connect(self.signal_unit_changed)

        self.multiple_chart_view = GridLine2D(self.multipleChart).setup_grid(nrows=8, ncols=15)
        self.list_chart_view = GridLine2D(self.listChart)

        self.recording_start_s, self.recording_step_s = 0, RECORDING_STEP_S
        self.update_timer = QTimer()
        self.update_timer.timeout.connect(self.update_canvas)

        self.logger = Logger.get_logger()
        self.logger.progress_signal.connect(self.update_progress)

        self.ui_view = None
        self.raw_handler = Raw(self)
        self.spike_handler = Spike(self)

        self.layout_ui = LayoutUi(self)
        self.layoutTbl.itemChanged.connect(self.layout_ui.handle_table_item_change)
        self.load_layout_names()

        self.loader = Loader()
        self.analysis_ui = AnalysisUi(self)

        self.load_analysis()

        self.show()

    def closeEvent(self, event):
        # Display a confirmation message box
        confirm_dialog = QMessageBox(self)
        confirm_dialog.setIcon(QMessageBox.Question)
        confirm_dialog.setWindowTitle('Confirm Close')
        confirm_dialog.setText('Are you sure you want to close the application?')
        confirm_dialog.setStandardButtons(QMessageBox.Yes | QMessageBox.No)

        result = confirm_dialog.exec_()

        if result == QMessageBox.Yes:
            event.accept()  # Close the application
        else:
            event.ignore()  # Continue running the application

    def load_file(self):
        if self.ui_view is not None:
            self.ui_view.select_file()

    def update_progress(self, msg, progress):
        self.progressBar.setValue(progress)
        self.progressLabel.setText(msg)

    def timer_start(self):
        self.update_timer.start(CLOCK_SPEED_MS)

    def timer_stop(self):
        if self.update_timer.isActive():
            self.update_timer.stop()
        else:
            self.recording_start_s = 0
            self.plot_view()

    def step_forward(self):
        if self.ui_view is not None:
            self.recording_start_s += self.recording_step_s * self.speedSelector.value()
            self.plot_view()

    def step_backward(self):
        if self.ui_view is not None:
            self.recording_start_s -= self.recording_step_s * self.speedSelector.value()
            self.recording_start_s = max(self.recording_start_s, 0)
            self.plot_view()

    def update_canvas(self):
        if self.ui_view is not None:
            self.step_forward()

    def plot_view(self):

        if self.ui_view is not None:
            if self.is_info_view_selected():
                self.ui_view.plot_info_view()
            elif self.is_single_view_selected():
                self.ui_view.plot_single_view()
            elif self.is_grid_view_selected():
                self.ui_view.plot_multiple_view()
            elif self.is_list_view_selected():
                self.ui_view.plot_list_view()

    def is_info_view_selected(self):
        return self.stackedWidget.currentWidget() == self.infoView

    def is_single_view_selected(self):
        return self.stackedWidget.currentWidget() == self.singleView

    def is_grid_view_selected(self):
        return self.stackedWidget.currentWidget() == self.gridView

    def is_list_view_selected(self):
        return self.stackedWidget.currentWidget() == self.listView

    def open_folder(self):
        folder_path = QtWidgets.QFileDialog.getExistingDirectory(self, "Select Folder", options=QtWidgets.QFileDialog.DontUseNativeDialog)
        if folder_path:
            self.load_files(folder_path)

    def load_files(self, folder_path):
        self.fileSelector.clear()
        self.raw_handler.load_files(folder_path)
        self.spike_handler.load_files(folder_path)
        self.analysisBtn.setEnabled(True)

        self.ui_view = None

    def raw_view(self):
        self.ui_view = self.raw_handler
        self.ui_view.select_view()

    def spike_view(self):
        self.ui_view = self.spike_handler
        self.ui_view.select_view()

    def select_info_view(self):
        self.stackedWidget.setCurrentWidget(self.infoView)
        self.optionStck.setCurrentWidget(self.emptyOptPage)

        if self.ui_view is not None:
            self.ui_view.plot_info_view()

    def config_view(self):
        self.stackedWidget.setCurrentWidget(self.configView)
        self.optionStck.setCurrentWidget(self.emptyOptPage)

    def analysis_view(self):
        self.stackedWidget.setCurrentWidget(self.analysisView)
        self.optionStck.setCurrentWidget(self.emptyOptPage)

    def select_single_view(self):
        self.stackedWidget.setCurrentWidget(self.singleView)
        if self.ui_view is not None:
            self.ui_view.plot_single_view()

    def select_grid_view(self):
        self.stackedWidget.setCurrentWidget(self.gridView)
        if self.ui_view is not None:
            self.ui_view.plot_multiple_view()

    def select_list_view(self):
        self.stackedWidget.setCurrentWidget(self.listView)
        if self.ui_view is not None:
            self.ui_view.plot_list_view()

    def extract_spikes(self):
        self.raw_handler.extract_spikes()

    def extract_all_spikes(self):
        self.raw_handler.extract_all_spikes()

    def run_kmeans(self):
        self.spike_handler.run_kmeans()

    def run_all_kmeans(self):
        self.spike_handler.run_all_kmeans()

    def reset_spike_classes(self):
        self.spike_handler.reset_spike_classes()

    def signal_unit_changed(self, changes):
        self.spike_handler.signal_unit_changed(changes)

    def save_spikes(self):
        self.spike_handler.save_spikes()

    def spike_stacked_or_ts(self, val):
        self.plot_view()

    def new_layout(self):
        self.layout_ui.new_layout()

    def delete_layout(self):
        self.layout_ui.delete_layout()

    def set_current_layout(self, selected):
        self.layout_ui.set_current_layout(selected)

    def select_layout(self, selected_name):
        self.layout_ui.select_layout(selected_name)

    def load_layout_names(self, selected_name=None):
        self.layout_ui.load_layout_names(selected_name)

    def plot_layout(self, name):
        self.layout_ui.plot_layout(name)

    def load_analysis(self):
        self.analysis_ui.load_analysis()

    def analysis_selected(self, item, index):
        self.analysis_ui.analysis_selected(item, index)

    def run_analysis(self):
        self.analysis_ui.run_analysis()

    def new_analysis(self):
        self.analysis_ui.new_analysis()

    def delete_analysis(self):
        self.analysis_ui.delete_analysis()

    def edit_analysis(self):
        self.analysis_ui.edit_analysis()

    def export_analysis(self):
        self.analysis_ui.export_analysis()

