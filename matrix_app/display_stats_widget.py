"""
small_matrix_app.matrix_app.display_stats_widget.py
Sets up screen for displays stats for a particular run
"""
import string
import sys
import random
from PyQt5.QtCore import Qt, QAbstractTableModel
from PyQt5.QtWidgets import (
    QVBoxLayout,
    QWidget,
    QHBoxLayout,
    QPushButton,
    QSizePolicy,
    QInputDialog,
    QLineEdit,
    QMessageBox,
    QLabel,
    QTableView,
    QApplication,
)

import numpy as np

from typing import Callable, List

from matrix_app.db_widget import DisplayData, RunData


# Functions as cache/display for calculated matrices/stats
class DisplayStatsPage(QWidget):
    def __init__(
        self,
        matrices: List[DisplayData] = None,
        run_data: RunData = None,
        parent=None,
    ):
        """
        Sets up screen for displays stats for a particular run
        Args:
        matrices -- the two entered matrices and their product, for populating a new run
        run_data -- all matrices/stats for a preexisting run, for populating DisplayStats with a pre-existing run
        parent -- parent of DisplayStatsPage
        """
        super().__init__(parent)
        self.run_name = ""
        self.display_data = []
        self.matrices = matrices
        self.run_data = run_data
        letters = string.ascii_lowercase
        result_str = "".join(random.choice(letters) for i in range(12))
        self.id = result_str
        self.display_only = False
        if self.run_data is not None:
            try:
                self.matrices = self.run_data.matrices
                self.display_data = self.run_data.stats
                self.display_only = True
            except Exception as e:
                self.matrices = []
        self._initUi()
        self.show()

    def onCalculate(self):
        """Calculates stats for the matrices, for populating a new run"""
        self._calculate_stats()
        self._display_calculated_stats()
        self.save_button.setText("Save Run with Stats!")
        self.calculate_current_stats_button.disconnect()

    def _initUi(self):

        self.full_display_layout = QHBoxLayout()
        self.setLayout(self.full_display_layout)

        self.save_button = QPushButton()
        self.save_button.setText("Save Run - Matrices A,B, and C")
        self.calculate_current_stats_button = QPushButton()
        self.calculate_current_stats_button.setText("Calculate Stats!")
        self.calculate_new_stats_button = QPushButton()
        self.calculate_new_stats_button.setText("Create New Run")
        self.calculate_current_stats_button.clicked.connect(self.onCalculate)

        calculations_label = QLabel()
        calculations_label.setText("Calculations!")
        calculations_label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        calculations_label.setAlignment(Qt.AlignCenter)

        self.data_display_widget = QWidget()
        self.data_display_layout = QVBoxLayout()
        self.data_display_widget.setLayout(self.data_display_layout)

        self.matrices_display_widget = QWidget()
        self.matrices_display_layout = QVBoxLayout()
        self.matrices_display_widget.setLayout(self.matrices_display_layout)

        self._display_matrices()

        bottom_widget = QWidget()
        vbox_bottom = QVBoxLayout()
        vbox_bottom.addWidget(self.matrices_display_widget)
        vbox_bottom.addWidget(self.calculate_current_stats_button)
        vbox_bottom.addWidget(self.calculate_new_stats_button)
        vbox_bottom.addWidget(self.save_button)
        bottom_widget.setLayout(vbox_bottom)

        self.full_display_layout.addWidget(bottom_widget)
        self.full_display_layout.addWidget(self.data_display_widget)

        if self.display_only:
            self._display_calculated_stats()
            self.save_button.hide()
            self.calculate_current_stats_button.hide()

    def _display_matrices(self):
        for datum in self.matrices:
            table_lable = QLabel()
            table_lable.setText(datum.label)
            table_widget = QTableView()
            table_widget.setWindowTitle(datum.label)
            table_widget.horizontalHeader().hide()
            table_widget.verticalHeader().hide()

            model = TableModel(datum.data.tolist())
            table_widget.setModel(model)
            table_widget.setContentsMargins(0, 0, 0, 0)
            table_widget.resizeColumnsToContents()
            table_widget.resizeRowsToContents()
            table_widget.adjustSize()
            datum_display_widget = QWidget()
            datum_display_layout = QVBoxLayout()
            datum_display_layout.setContentsMargins(0, 0, 0, 0)
            datum_display_layout.addWidget(table_lable)
            datum_display_layout.addWidget(table_widget)
            datum_display_widget.setLayout(datum_display_layout)

            self.matrices_display_layout.addWidget(datum_display_widget)
        self.adjustSize()

    def _display_calculated_stats(self):
        wig_list = []
        for datum in self.display_data:
            table_lable = QLabel()
            table_lable.setText(datum.label)
            table_widget = QTableView()
            table_widget.setWindowTitle(datum.label)
            table_widget.horizontalHeader().hide()
            table_widget.verticalHeader().hide()

            model = TableModel(datum.data.tolist())
            table_widget.setModel(model)
            table_widget.setContentsMargins(0, 0, 0, 0)
            table_widget.resizeColumnsToContents()
            table_widget.resizeRowsToContents()
            table_widget.adjustSize()
            datum_display_widget = QWidget()
            datum_display_layout = QVBoxLayout()
            datum_display_layout.setContentsMargins(0, 0, 0, 0)
            datum_display_layout.addWidget(table_lable)
            datum_display_layout.addWidget(table_widget)
            datum_display_widget.setLayout(datum_display_layout)
            wig_list.append(datum_display_widget)
        self.adjustSize()
        self.save_button.show()
        self.calculate_current_stats_button.hide()

        # Grid Like Pattern
        sqrt = int(np.ceil(np.sqrt(len(self.display_data))))
        for r in range(sqrt):
            w = QWidget()
            hbox = QHBoxLayout()
            for c in range(sqrt):
                if len(wig_list) > 0:
                    hbox.addWidget(wig_list.pop())
            w.setLayout(hbox)
            self.data_display_layout.addWidget(w)

    def _calculate_stats(self):
        if len(self.display_data) > 1:
            return
        if len(self.matrices) < 2:
            raise Exception("Cannot compute statistics without 2 matrices")
        A = self.matrices[0].data
        B = self.matrices[1].data
        C = A.dot(B)

        # precalculate cumulative prod since it's the slowest
        cprod = C.cumprod()
        cprodc = C.cumprod(axis=0)
        cprodr = C.cumprod(axis=1)

        # Across all entries
        if not cprod.max() > sys.maxsize:
            self.display_data.append(DisplayData("Cumulative Product Matrix ", cprod))
        else:
            self.display_data.append(
                DisplayData("Cumulative Product Too Large For Full Display", cprod)
            )

        self.display_data.append(DisplayData("Minimum Value in Matrix", C.min()))
        self.display_data.append(DisplayData("Mean across Matrix", C.mean()))
        self.display_data.append(DisplayData("Max across Matrix", C.max()))

        # Across columns
        if not cprodc.max() > sys.maxsize:
            self.display_data.append(
                DisplayData("Cumulative Product down each Column", cprodc)
            )
        else:
            self.display_data.append(
                DisplayData(
                    "Cumulative Product Down Each Column Too Large For Full Display",
                    cprodc,
                )
            )

        self.display_data.append(DisplayData("Minimum Value per Column", C.min(axis=0)))
        self.display_data.append(DisplayData("Mean of each Column", C.mean(axis=0)))
        self.display_data.append(DisplayData("Max of each Column", C.max(axis=0)))

        # Across rows
        if not cprodr.max() > sys.maxsize:
            self.display_data.append(
                DisplayData("Cumulative Product across each Row ", cprodr)
            )
        else:
            self.display_data.append(
                DisplayData(
                    "Cumulative Product Across Each Row Too Large For Full Display",
                    cprodr,
                )
            )
        self.display_data.append(
            DisplayData("Minimum Value per Row", C.min(axis=1).reshape(-1, 1))
        )  # ROW VECTOR to COL
        self.display_data.append(
            DisplayData("Mean of each Row", C.mean(axis=1).reshape(-1, 1))
        )  # ROW VECTOR to COL
        self.display_data.append(
            DisplayData("Max of each Row", C.max(axis=1).reshape(-1, 1))
        )  # ROW VECTOR to COL

    def save_display(self, save_method: Callable):
        """Saved matrices and stats in a new run to disk
        Args:
            saved_method(Callable): Method called to save the data to disk.
            save_method should save to disk via the db_widget

        """
        msg = QMessageBox()
        self.x = msg

        if self.run_name != "":
            self.run_data = RunData(
                self.run_name, self.matrices, self.display_data, random=self.id
            )
            err = save_method(self.run_data)
            if err is None:
                self.save_button.hide()
            else:
                self.x.setText("ERROR: Run not saved: " + str(err))
                self.x.exec_()
            return

        run_name, ok_pressed = QInputDialog.getText(
            self,
            "Enter run name",
            "Must be alphanumerical:",
            QLineEdit.Normal,
            "",
        )
        if ok_pressed:
            if run_name == "":
                self.x.setText("Cannot give empty run name. Run not saved.")
                self.x.exec_()
                return
            if run_name.isalnum():
                self.run_data = RunData(
                    run_name, self.matrices, self.display_data, random=self.id
                )
                err = save_method(self.run_data)
                if err is None:
                    self.run_name = run_name
                    self.save_button.hide()
                    return
                self.x.setText(
                    "Sorry! There is already another run saved by this name - You cannot save the same run twice!"
                )
                self.x.exec_()
                return
            else:
                self.x.setText("Run name must be alphanumeric. Run not saved.")
                self.x.exec_()
                return

            self.save_button.hide()


# copied TableModel modified from https://www.learnpyqt.com/courses/model-views/qtableview-modelviews-numpy-pandas/
class TableModel(QAbstractTableModel):
    def __init__(self, data):
        """ Table Model is used to cache new run calculated statistics until they are saved to disk"""
        super(TableModel, self).__init__()
        self._data = data

    def data(self, index, role):
        if role == Qt.DisplayRole:
            # See below for the nested-list data structure.
            # .row() indexes into the outer list,
            # .column() indexes into the sub-list
            if isinstance(self._data, int) or isinstance(self._data, float):
                return self._data
            if isinstance(self._data[0], int) or isinstance(self._data[0], float):
                return self._data[index.column()]
            return self._data[index.row()][index.column()]

    # Override
    def rowCount(self, index):
        # The length of the outer list.
        if isinstance(self._data, int) or isinstance(self._data, float):
            return 1
        if isinstance(self._data[0], int) or isinstance(self._data[0], float):
            return 1
        return len(self._data)

    # Override
    def columnCount(self, index):
        # The following takes the first sub-list, and returns
        # the length (only works if all rows are an equal length)
        if isinstance(self._data, int) or isinstance(self._data, float):
            return 1
        if isinstance(self._data[0], int) or isinstance(self._data[0], float):
            return len(self._data)
        return len(self._data[0])


# def main():
#
#     app = QApplication(sys.argv)
#     win = DisplayStatsPage( [[],[]])
#     win.show()
#     print("ship")
#     sys.exit(app.exec_())
#
#
# if __name__ == '__main__':
#    main()
