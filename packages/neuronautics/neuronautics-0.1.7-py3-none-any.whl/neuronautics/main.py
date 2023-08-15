from PyQt5 import QtWidgets
import sys
import os
module_directory = os.path.dirname(os.path.abspath(__file__))
sys.path.append(module_directory+'/..')

import my_resources

from neuronautics.ui.neuronautics_ui import NeuronauticsUi

def main():
    app = QtWidgets.QApplication(sys.argv)

    window = NeuronauticsUi()

    app.exec_()

if __name__ == '__main__':
    main()