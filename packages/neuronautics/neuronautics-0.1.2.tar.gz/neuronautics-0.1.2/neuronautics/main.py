from PyQt5 import QtWidgets
import sys
import resources

from neuronautics.ui.neuronautics_ui import NeuronauticsUi


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)

    window = NeuronauticsUi()

    app.exec_()