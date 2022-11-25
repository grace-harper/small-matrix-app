"""
small_matrix_app.matrix_app.saved_runs_widget.py
Saved Runs Widget displays the names of all previous saved runs
in a list to the user can click on the run he/she wants
to see the stats from.
"""

from PyQt5.QtWidgets import (
    QApplication,
    QWidget,
    QScrollArea,
    QVBoxLayout,
    QGroupBox,
    QLabel,
    QPushButton,
    QFormLayout,
)

from typing import Callable, List


class SavedRunsPage(QWidget):
    def __init__(self, _previous_runs: List[str], display_method: Callable):
        """Will list all previous runs in the UI so the user can click on the run he/she wants to see the stats from.
        Doing so will trigger the display_method which, if successful, will result in a new central widget for the
        Main Window that displays the stats associated with that run

        display_method -- method connected to each previous-run button in the UI. The method triggers a new
        central widget displays the stats related to the run on the button to be displayed in the MainWindow
        """
        super().__init__()
        self._previous_runs = _previous_runs
        self._title = "Previous Runs"
        self._button_list = []
        self.display_method = display_method
        self._initUi()

    def _initUi(self):
        self.setWindowTitle(self._title)
        form_layout = QFormLayout()
        group_box = QGroupBox()
        label_list = []
        combo_list = []
        for i in range(len(self._previous_runs)):
            label_list.append(QLabel())
            button = QPushButton(self._previous_runs[i])
            button.setText(self._previous_runs[i])
            button.clicked.connect(
                lambda state, x=str(self._previous_runs[i]): self.display_method(x)
            )
            combo_list.append(button)
            self._button_list.append(button)
            form_layout.addRow(label_list[i], combo_list[i])
        group_box.setLayout(form_layout)
        scroll = QScrollArea()
        scroll.setWidget(group_box)
        scroll.setWidgetResizable(True)
        scroll_layout = QVBoxLayout(self)
        scroll_layout.addWidget(scroll)
        self.setLayout(scroll_layout)
        self.adjustSize()
