from neuronautics.analysis.loader import Loader
from neuronautics.analysis.type.abstract_analysis import AnalysisType
from neuronautics.analysis.analysis_creator import AnalysisCreatorUi

# plotters
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas

# logger
from neuronautics.utils.logger import Logger

# pyqt
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QTreeWidgetItem

from neuronautics.utils.singleton import Singleton
from neuronautics.ui.helpers import clear_layout


class AnalysisUi(metaclass=Singleton):
    me = None

    def __init__(self, ui):
        self.ui = ui
        self.current_analysis = None
        self.current_analysis_params = None
        self.current_fig = None
        self.current_fig_metadata = None

    def load_analysis(self):
        tree = self.ui.analysisTree.invisibleRootItem()
        self.ui.loader.load()
        analysis = self.ui.loader.get_types()

        analysis_by_type = dict()
        for name, analysis_type in analysis.items():
            aux = analysis_by_type.get(analysis_type.value, [])
            aux.append(name)
            analysis_by_type[analysis_type.value] = aux

        for child_id in range(tree.childCount()):
            child = tree.child(child_id)
            for name in analysis_by_type.get(child.text(0), []):
                QTreeWidgetItem(child, [name])
            child.setExpanded(True)

    def analysis_selected(self, item, index):
        analysis_name = item.text(0)
        self.current_analysis = analysis_name
        loader = Loader()
        loader.load()
        handle = loader.analysis_handle.get(analysis_name)
        if handle:
            params = handle.get_input_params()
            layout = self.ui.inputAnalysisLyt
            clear_layout(layout)

            self.current_analysis_params = {}
            field_builder = dict(
                int=self._setup_int_field,
                float=self._setup_float_field,
                bool=self._setup_bool_field,
                list=self._setup_list_field
            )
            for param in params:
                label = QtWidgets.QLabel(param['name'])
                field = field_builder.get(param['type'])(param)
                self.current_analysis_params[param['name']] = field
                layout.addRow(label, field)

    @staticmethod
    def _setup_list_field(param):
        field = QtWidgets.QComboBox()
        field.addItems(param['values'])
        field.setCurrentText(param['default'])
        return field

    @staticmethod
    def _setup_bool_field(param):
        field = QtWidgets.QCheckBox()
        field.setChecked(param['default'])
        return field

    @staticmethod
    def _setup_float_field(param):
        field = QtWidgets.QDoubleSpinBox()
        field.setMinimum(param['min'])
        field.setMaximum(param['max'])
        field.setValue(param.get('default', param['min']))
        field.setSingleStep((param['max'] - param['min']) / 10)
        return field

    @staticmethod
    def _setup_int_field(param):
        field = QtWidgets.QSpinBox()
        field.setMinimum(param['min'])
        field.setMaximum(param['max'])
        field.setValue(param.get('default', param['min']))
        return field

    @staticmethod
    def _get_value(field):
        if isinstance(field, QtWidgets.QCheckBox):
            return field.isChecked()
        elif isinstance(field, QtWidgets.QComboBox):
            return field.currentText()
        return field.value()

    def run_analysis(self):
        current_analysis_params = {name: self._get_value(field) for name, field in self.current_analysis_params.items()}
        handle = Loader().analysis_handle.get(self.current_analysis)

        fig = handle.plot(spikes=self.ui.spike_handler.all_data(), **current_analysis_params)

        clear_layout(self.ui.outputAnalysisLyt)
        canvas = FigureCanvas(fig)
        self.ui.outputAnalysisLyt.addWidget(canvas)

        self.current_fig = fig
        self.current_fig_metadata = current_analysis_params
        self.ui.analysisExportBtn.setEnabled(True)

    def new_analysis(self):
        analysis_ui = AnalysisCreatorUi()
        if analysis_ui.exec_():
            self.clear_analysis_tree()
            self.load_analysis()

    def clear_analysis_tree(self):
        tree = self.ui.analysisTree.invisibleRootItem()
        for i in reversed(range(tree.childCount())):
            for j in reversed(range(tree.child(i).childCount())):
                tree.child(i).takeChild(j)

    def delete_analysis(self):
        selected_analysis = self.ui.analysisTree.currentItem().text(0)
        self.ui.loader.delete(selected_analysis)
        self.clear_analysis_tree()
        self.load_analysis()

    def edit_analysis(self):
        selected_analysis = self.ui.analysisTree.currentItem().text(0)
        from neuronautics.utils.helpers import open_external_editor
        path = self.ui.loader.get_analysis_path(selected_analysis)
        if selected_analysis:
            open_external_editor(path)

    def export_analysis(self):
        if self.current_fig is not None:
            filename, filt = QtWidgets.QFileDialog.getSaveFileName(self.ui, "Save figure",
                                                                   options=QtWidgets.QFileDialog.DontUseNativeDialog,
                                                                   filter='Figure (*.png)')
            if filename and not filename.endswith('.png'):
                filename = filename + '.png'
            metadata = {f'PARAM: {k}': str(v) for k,v in self.current_fig_metadata.items()}
            self.current_fig.savefig(filename, format='png', transparent=True,
                                     backend='agg',
                                     metadata=metadata)
