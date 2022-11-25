"""
small_matrix_app.matrix_app.home_screen_widget.py
Creates the widget for the home screen page
"""

import sys

from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QHBoxLayout, QPushButton, QVBoxLayout


class HomeScreenPage(QtWidgets.QWidget):
    def __init__(self, parent=None):
        """Set up home screen display"""
        super().__init__(parent)
        self._initUi()

    def _initUi(self):
        hbox = QHBoxLayout()
        self.saved_runs_button = QPushButton()
        self.saved_runs_button.setText("Saved Runs")

        self.create_run_button = QPushButton()
        self.create_run_button.setText("New Run")

        hbox.addWidget(self.saved_runs_button)
        hbox.addWidget(self.create_run_button)

        hwidget = QtWidgets.QWidget()
        hwidget.setLayout(hbox)

        self.setLayout(hbox)


def main():
    app = QtWidgets.QApplication(sys.argv)
    win = HomeScreenPage()
    win.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
