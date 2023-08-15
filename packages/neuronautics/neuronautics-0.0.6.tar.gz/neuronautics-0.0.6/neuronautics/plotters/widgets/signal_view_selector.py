from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QDialog, QDialogButtonBox
from PyQt5.QtGui import QColor
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QCheckBox
from neuronautics.plotters.widgets.signal_line import SignalLine


class SignalViewSelector(QDialog):
    NEW = 9999
    CANCEL = -9999

    def __init__(self, signal_ids, signal_visible=None, parent=None):
        super().__init__(parent, Qt.CustomizeWindowHint)

        app = QApplication.instance()
        main_app_stylesheet = app.activeWindow().styleSheet()

        if signal_visible is None:
            signal_visible = [True] * len(signal_ids)

        self.setStyleSheet(main_app_stylesheet)

        widget = QWidget()
        layout = QVBoxLayout(widget)
        self.setLayout(layout)

        # Add buttons to the grid
        signal_ids = sorted(list(signal_ids))
        self.checkbox = {}

        for ix, (signal_id, visible) in enumerate(zip(signal_ids, signal_visible)):
            if signal_id >= 0:
                chk_box = QCheckBox(f"{signal_id}")
                chk_box.setChecked(visible)
                self._style_box(chk_box, QColor(*SignalLine.color(signal_id)))

                layout.addWidget(chk_box)
                self.checkbox[signal_id] = chk_box

        chk_box = QCheckBox(f"Noise")
        chk_box.setChecked(True)
        self._style_box(chk_box, QColor(*SignalLine.color(-1)))
        layout.addWidget(chk_box)
        self.checkbox[-1] = chk_box

        buttonBox = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)

        buttonBox.accepted.connect(self.accept)
        buttonBox.rejected.connect(self.reject)

        layout.addWidget(buttonBox)

        # Set the widget as the message box's layout
        self.layout().addWidget(widget)

    def _style_box(self, chk, background_color):
        style = [f"background-color: {background_color.name()}",
                 "width: 50px",
                 f"color: {background_color.darker(240).name()}",
                 f"border: 2px solid {background_color.darker(120).name()}"]
        chk.setStyleSheet(";".join(style))

    def accept(self):
        self.done(1)

    def reject(self):
        self.done(-1)

    def get_selected(self):
        return {id: chk.isChecked() for id, chk in self.checkbox.items()}
