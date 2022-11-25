"""
small_matrix_app.matrix_app.main_window.py
Window is the display window for the matrix_app.
The same instance of this class is used throughout the entire lifetime of the app.
The different "screens" of the application are achieved by changing out Window's central widget.
The Main Window is responsible for hooking up change-screen buttons in whichever widget it sets as its centralwidget.
"""

import sys

from PyQt5 import QtCore
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QAction, QDesktopWidget, QMessageBox
from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtWidgets import QStatusBar
from PyQt5.QtWidgets import QToolBar

from matrix_app.all_exceptions import (
    CriticalFailure,
    FailureMessage,
    InternalDbError,
)
from matrix_app.db_widget import DatabaseModel, DisplayData, RunData
from matrix_app.display_stats_widget import DisplayStatsPage
from matrix_app.home_screen_widget import HomeScreenPage
from matrix_app.saved_runs_widget import SavedRunsPage
from matrix_app.matrix_entry_widget import MatrixEntryPage

# from matrix_app.matrix_entry_widget import MatrixEntryPage

from typing import List


class Window(QMainWindow):
    """Main Window."""

    def __init__(self, db_name="SavedRuns", parent=None):
        """Sets up and display Window and places Homepage  Widget as the central widget"""
        super().__init__(parent)
        self._init_db(db_name)
        self._initUi()
        self.show()

    def _initUi(self):
        self.resize(QDesktopWidget().availableGeometry(self).size() * 0.7)
        self.setWindowTitle("Matrix Stats")
        self._create_tool_bar()
        self._create_status_bar()
        self._display_home_screen_page()
        # self.displayMatrixEntryPage()

    def _init_db(self, db_name) -> object:
        try:
            self.data_run_model = DatabaseModel(db_name)
        except CriticalFailure as err:
            ok = QMessageBox().question(
                self,
                "Info Box",
                str(err) + " System will shut down.",
                QMessageBox.Ok,
            )
            self.close()

    # Main Menu UI Components
    def _create_tool_bar(self):
        self.tools = QToolBar()
        self.addToolBar(self.tools)
        self.tools.addAction("Exit", self.close)

        self.home_screen_page_action = QAction("Return to Home Scren", self)
        self.home_screen_page_action.setStatusTip(
            "Click me to go back to the home screen!"
        )
        self.home_screen_page_action.triggered.connect(self._display_home_screen_page)
        self.tools.addAction(self.home_screen_page_action)

        self.saved_runs_page_action = QAction("View Saved Runs", self)
        self.saved_runs_page_action.setStatusTip("Click me to view your saved runs!")
        self.saved_runs_page_action.triggered.connect(self._display_saved_runs_page)
        self.tools.addAction(self.saved_runs_page_action)

        self.resize_screen_action = QAction("Default Screensize")
        self.resize_screen_action.setStatusTip(
            "Click me to make me 70% of your screen!"
        )
        self.resize_screen_action.triggered.connect(self.resize_me)
        self.tools.addAction(self.resize_screen_action)

    def _create_status_bar(self):
        status = QStatusBar()
        status.showMessage("hi!")
        self.setStatusBar(status)

    def resize_me(self):
        """ Sets the Window size to 70% of the current screen"""
        self.resize(QDesktopWidget().availableGeometry(self).size() * 0.7)

    # Controller-View
    # Choose to instantiate a new central widget for each screen change since
    # there is no reason to remember widget state

    def _display_matrix_entry(self):
        self.matrix_entry_page = MatrixEntryPage()

        self.matrix_entry_page.calculate_button.clicked.connect(
            self._matrix_entry_page_on_submit_matrices_button_clicked
        )

        self.setCentralWidget(self.matrix_entry_page)

    def _display_home_screen_page(self):
        self.home_screen_page = HomeScreenPage()

        self.home_screen_page.create_run_button.clicked.connect(
            self._display_matrix_entry
        )
        self.home_screen_page.saved_runs_button.clicked.connect(
            self._display_saved_runs_page
        )

        self.setCentralWidget(self.home_screen_page)

    def _display_saved_runs_page(self):
        self.saved_runs_page = SavedRunsPage(
            self.data_run_model.get_previous_runs(),
            self._saved_runs_page_on_display_button_clicked,
        )

        self.setCentralWidget(self.saved_runs_page)

    def _display_display_stats_page(
        self, matrices: List[DisplayData] = None, run_data: RunData = None
    ):
        self.display_stats_page = DisplayStatsPage(matrices=matrices, run_data=run_data)

        self.display_stats_page.save_button.clicked.connect(
            lambda state, x=self.data_run_model.save_run: self.display_stats_page.save_display(
                x
            )
        )
        self.display_stats_page.calculate_new_stats_button.clicked.connect(
            self._display_matrix_entry
        )

        self.setCentralWidget(self.display_stats_page)

    # Passing Data Across Central Widgets Functions

    def _saved_runs_page_on_display_button_clicked(self, saved_run_name: str):
        try:
            run_data = self.data_run_model.load_run(saved_run_name)
            self._display_display_stats_page(run_data=run_data)
        except InternalDbError as fm:
            msg = QMessageBox()
            self.x = msg
            self.x.setText("ERROR: Run not saved: " + str(fm))
            self.x.exec_()
        except Exception as e:
            msg = QMessageBox()
            self.x = msg
            self.x.setText("ERROR: Run not saved: " + str(e))
            self.x.exec_()

    def _matrix_entry_page_on_submit_matrices_button_clicked(self):
        dd, err = self.matrix_entry_page.calculate_matrix()
        if err is not None:
            pass
        else:
            self._display_display_stats_page(matrices=dd)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = Window()
    win.show()
    sys.exit(app.exec_())
