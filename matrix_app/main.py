"""small_matrix_app.matrix_app.main.py
Starts/Runs Application
"""

import sys

from PyQt5.QtCore import QTimer
from PyQt5.QtWidgets import QApplication

from matrix_app.main_window import Window

if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = Window()
    win.show()
    timer = QTimer()
    timer.timeout.connect(lambda: None)
    timer.start(100)
    exit_no = app.exec_()
    sys.exit(exit_no)
