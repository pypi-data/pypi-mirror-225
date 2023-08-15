from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QDialog
from PyQt5.QtGui import QColor
from PyQt5.QtWidgets import QApplication, QWidget, QGridLayout, QPushButton
from neuronautics.plotters.widgets.signal_line import SignalLine


N_ROWS = 3


class SignalUnitSelector(QDialog):
    NEW = 9999
    NOISE = -1
    CANCEL = -9999

    def __init__(self, signal_ids, parent=None):
        super().__init__(parent, Qt.CustomizeWindowHint)

        app = QApplication.instance()
        main_app_stylesheet = app.activeWindow().styleSheet()

        self.setStyleSheet(main_app_stylesheet)
        self.setAttribute(Qt.WA_TranslucentBackground)

        # Set the window title and message text
        self.setWindowTitle("Manual sorting")

        widget = QWidget()
        layout = QGridLayout(widget)
        self.setLayout(layout)

        # Add buttons to the grid
        signal_ids = sorted(list(signal_ids))

        for ix, signal_id in enumerate(signal_ids):
            btn = QPushButton(f"{signal_id}")
            self._style_button(btn, QColor(*SignalLine.color(signal_id)))

            layout.addWidget(btn, int(ix/N_ROWS), ix % N_ROWS)
            btn.clicked.connect(lambda _, btn=btn: self.handle_button_click(btn))

        btn_noise = QPushButton(f"Noise")
        self._style_button(btn_noise, QColor(*SignalLine.color(-1)))

        btn_new = QPushButton(f"New")
        self._style_button(btn_new, QColor(255, 255, 255))

        layout.addWidget(btn_noise, int(ix/N_ROWS) + 1, 0)
        layout.addWidget(btn_new, int(ix/N_ROWS) + 1, 1)

        btn_noise.clicked.connect(lambda _, btn=btn_noise: self.handle_button_click(btn))
        btn_new.clicked.connect(lambda _, btn=btn_new: self.handle_button_click(btn))

        btn_cancel = QPushButton("Cancel", self)
        self._style_button(btn_cancel, QColor(255, 255, 255))

        layout.addWidget(btn_cancel, int(ix/N_ROWS) + N_ROWS, 0, 1, N_ROWS)  # Span two columns for the Cancel button

        # Connect the Cancel button click to the reject slot
        btn_cancel.clicked.connect(self.reject)
        btn_cancel.clicked.connect(lambda _, btn=btn_cancel: self.handle_button_click(btn))

        # Set the widget as the message box's layout
        self.layout().addWidget(widget)

    def _style_button(self, btn, background_color):
        style = [f"background-color: {background_color.name()}",
                 "width: 50px",
                 f"color: {background_color.darker(240).name()}",
                 f"border: 2px solid {background_color.darker(120).name()}"]
        btn.setStyleSheet(";".join(style))

    def handle_button_click(self, btn):
        if btn.text().upper() == 'NOISE':
            self.done(SignalUnitSelector.NOISE)
        elif btn.text().upper() == 'NEW':
            self.done(SignalUnitSelector.NEW)
        elif btn.text().upper() == 'CANCEL':
            self.done(SignalUnitSelector.CANCEL)
        else:
            self.done(int(float(btn.text())))
