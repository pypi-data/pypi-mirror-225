import resources  # this import is required for loading icons in ui

# logger
from neuronautics.utils.logger import Logger

# pyqt
from PyQt5 import QtWidgets, uic
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QMessageBox

from neuronautics.utils.singleton import Singleton
from neuronautics.config.layout import Layout


class LayoutCreationUi(QtWidgets.QDialog):
    def __init__(self):
        super(LayoutCreationUi, self).__init__()
        self.setWindowFlags(Qt.CustomizeWindowHint | Qt.WindowCloseButtonHint)

        uic.loadUi('ui/layout-creation.ui', self)

        self.show()

    def create_layout(self):
        self.done(1)

    def get_data(self):
        name = self.layout_name.text()
        cols, rows = self.num_cols.value(), self.num_rows.value()
        return name, cols, rows


class LayoutUi(metaclass=Singleton):

    def __init__(self, ui):
        self.ui = ui
        self.layout = Layout()

    def new_layout(self):
        layout_ui = LayoutCreationUi()
        result = layout_ui.exec_()

        if result == QtWidgets.QDialog.Accepted:
            name, cols, rows = layout_ui.get_data()
            self.layout.new(name, cols, rows)
            self.load_layout_names(name)

    def delete_layout(self):
        layout_name = self.ui.layoutSelector.currentText()
        if layout_name:
            result = QMessageBox.question(self.ui, "Confirmation", "Are you sure you want to delete this item?",
                                          QMessageBox.Yes | QMessageBox.No, QMessageBox.No)

            if result == QMessageBox.Yes:
                self.layout.delete(layout_name)
                self.load_layout_names()

    def set_current_layout(self, selected):
        if selected > 0:
            layout_name = self.ui.layoutSelector.currentText()
            self.layout.set_current_layout(layout_name)

    def select_layout(self, selected_name):
        layout_names = self.layout.names()

        selected_ix = 0
        for ix, name in enumerate(layout_names):
            if name == selected_name:
                selected_ix = ix
        if len(layout_names) > 0:
            self.ui.layoutSelector.setCurrentIndex(selected_ix)
            self.plot_layout(layout_names[selected_ix])
            self.ui.currentLayoutCheck.setChecked(self.layout.is_current_layout(layout_names[selected_ix]))

    def load_layout_names(self, selected_name=None):
        layout_names = self.layout.names()
        self.ui.layoutSelector.clear()
        for ix, name in enumerate(layout_names):
            self.ui.layoutSelector.addItem(name)
        self.select_layout(selected_name)

    def plot_layout(self, name):
        self.ui.layoutTbl.itemChanged.disconnect()

        cols, rows = self.layout.get_shape(name)
        cell_values = self.layout.get_layout(name)
        column_headers = self.layout.column_headers(cols)
        row_headers = self.layout.row_headers(rows)

        self.ui.layoutTbl.setRowCount(rows)
        self.ui.layoutTbl.setColumnCount(cols)

        for col, label in enumerate(column_headers):
            self.ui.layoutTbl.setHorizontalHeaderItem(col, QtWidgets.QTableWidgetItem(label))
        for row, label in enumerate(row_headers):
            self.ui.layoutTbl.setVerticalHeaderItem(row, QtWidgets.QTableWidgetItem(label))

        for col in range(cols):
            self.ui.layoutTbl.setColumnWidth(col, 80)
            for row in range(rows):
                item = QtWidgets.QTableWidgetItem(cell_values[row][col])
                item.setFlags(item.flags() | Qt.ItemIsEditable)  # Make the item editable
                self.ui.layoutTbl.setItem(row, col, item)

        self.ui.layoutTbl.itemChanged.connect(self.handle_table_item_change)

    def handle_table_item_change(self, item):
        layout_name = self.ui.layoutSelector.currentText()
        tab = self.ui.layoutTbl
        col, row = tab.columnCount(), tab.rowCount()

        cell_values = [[tab.item(r, c).text() for c in range(col)] for r in range(row)]

        self.layout.update(layout_name, cell_values)
        self.plot_layout(layout_name)