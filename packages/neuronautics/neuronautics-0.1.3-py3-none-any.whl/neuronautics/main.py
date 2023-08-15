from PyQt5 import QtWidgets
import sys
import resources

from neuronautics.ui.neuronautics_ui import NeuronauticsUi

def main():
    app = QtWidgets.QApplication(sys.argv)

    window = NeuronauticsUi()

    app.exec_()

if __name__ == '__main__':
    main()