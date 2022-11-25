"""
small_matrix_app.tests.matrix_entry_widget.py
Creates the screen for entering and submitting matrices to be multiplied together
"""
import sys

from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import (
    QVBoxLayout,
    QSpinBox,
    QGridLayout,
    QWidget,
    QHBoxLayout,
    QPushButton,
    QFormLayout,
    QTableWidget,
    QTableWidgetItem,
    QMessageBox,
    QLabel,
)

from typing import List
import numpy as np
import random

from matrix_app.all_exceptions import FailureMessage
from matrix_app.db_widget import DisplayData


class MatrixEntryPage(QtWidgets.QWidget):
    def __init__(self, parent=None):
        """
        MatrixEntryPage displays empty matrices that the use can fill in by hand. It also displays
        'Generate Random Matrices' button, which automatically fills in the matrices with random ints between 0 and 100.
        It also displays a 'CALCULATE Matrix1 x Matrix2 PRODUCT' button which will result in a new central widget
        for the MainWindow where stats for the inputted matrices can be generated.
        """
        # initAllScreens https://stackoverflow.com/questions/38923978/object-going-out-of-scope-and-being-garbage-collected-in-pyside-pyqt
        super().__init__(parent)
        self._initUi()
        self.show()

    def _initUi(self):
        self.submission_box_right = SubmitMatrixBox()
        self.submission_box_left = SubmitMatrixBox()
        self.matrix_entry_left = MatrixEntry("Matrix1")
        self.matrix_entry_right = MatrixEntry("Matrix2")

        self.generate_random_matrix_button = QPushButton()
        self.generate_random_matrix_button.setText("Generate Random Matrices")
        self.calculate_button = QPushButton()
        self.calculate_button.setText("CALCULATE Matrix1 x Matrix2 PRODUCT")

        submit_entry_widget = QWidget()
        submit_entry_layout = QGridLayout()
        submit_entry_layout.addWidget(self.submission_box_right, *(0, 1))
        submit_entry_layout.addWidget(self.matrix_entry_right, *(1, 1))
        submit_entry_layout.addWidget(self.submission_box_left, *(0, 0))
        submit_entry_layout.addWidget(self.matrix_entry_left, *(1, 0))
        submit_entry_widget.setLayout(submit_entry_layout)

        full_layout = QFormLayout()
        full_layout.addWidget(submit_entry_widget)

        full_layout.addWidget(self.generate_random_matrix_button)
        full_layout.addWidget(self.calculate_button)
        self.setLayout(full_layout)

        # Buttons

        # Resize matrix entries accordingly
        self.submission_box_right.choose_dimen_button.clicked.connect(
            lambda state, x=self.submission_box_right, y=self.matrix_entry_right: self._resize_matrix_entry(
                x, y
            )
        )
        self.submission_box_left.choose_dimen_button.clicked.connect(
            lambda state, x=self.submission_box_left, y=self.matrix_entry_left: self._resize_matrix_entry(
                x, y
            )
        )
        self.generate_random_matrix_button.clicked.connect(self._create_random_matrix)

    def _create_random_matrix(self):
        """ Creates and displays two randomly sized matrices for input matrices"""
        match_dim = random.randint(1, 10)
        d1_size = random.randint(1, 10)
        d2_size = random.randint(1, 10)

        self.matrix_entry_left.randomize_self(d1_size, match_dim)
        self.matrix_entry_right.randomize_self(match_dim, d2_size)
        self.matrix_entry_left.show()
        self.matrix_entry_right.show()

    def _resize_matrix_entry(self, sub_box, mat_ent) -> (bool, str):
        dim_tup = sub_box.get_dimensions()
        mat_ent.resize_self(dim_tup[0], dim_tup[1])
        mat_ent.show()

    def calculate_matrix(self) -> ([DisplayData], str):
        """Calculates the product of self.matrix_entry_left with self.matrix_entry_right.
        Returns the two input matrices and the product
        """
        m1, fm1 = self.matrix_entry_left.return_matrix()
        m2, fm2 = self.matrix_entry_right.return_matrix()
        msg = QMessageBox()
        msg.setText(
            "There was an error computing the matrix product.\nREMINDERS: Make sure your matrices have valid dimensions (mxn, nxk). Make sure your entries are valid floats/ints."
        )

        if fm1 is not None:
            msg.setText(
                "There was an error computing the matrix product.\nREMINDERS: Make sure your matrices have valid dimensions (mxn, nxk). Make sure your entries are valid floats/ints. "
                + str(fm1)
            )
            self.x = msg.exec_()
            return [], fm1
        if fm2 is not None:
            msg.setText(
                "There was an error computing the matrix product.\nREMINDERS: Make sure your matrices have valid dimensions (mxn, nxk). Make sure your entries are valid floats/ints. "
                + str(fm2)
            )
            self.x = msg.exec_()
            return [], fm2
        try:
            m1 = np.array(m1)
            m2 = np.array(m2)
            m3 = m1.dot(m2)
        except Exception as e:
            msg.setWindowTitle("Error! We can't compute the product of these matrices!")
            msg.setText(
                "We got an error trying use your input for the matrix product: "
                + str(e)
            )
            self.x = msg.exec_()
            return [], FailureMessage(str(e))

        dd = []
        dd.append(DisplayData("A", m1))
        dd.append(DisplayData("B", m2))
        dd.append(DisplayData("C", m3))
        self.show()
        return dd, None


class SubmitMatrixBox(QtWidgets.QWidget):
    def __init__(self, parent=None):
        """Creates submission box for choosing input matrix dimensions"""
        super().__init__(parent)
        self._initUi()
        self.show()

    def get_dimensions(self) -> (int, int):
        """Gets and returns the matrix dimension values from the input spinboxes
        Default return value is (4,4)
        """
        if self.sp1.value() is None or self.sp2.value() is None:
            return (4, 4)
        return (self.sp1.value(), self.sp2.value())

    def _initUi(self):
        # Name and Submit Button
        name_label = QLabel()
        name_label.setText("Choose Matrix Dimensions")
        name_label.setAlignment(QtCore.Qt.AlignCenter)

        self.info_label = QLabel()
        self.info_label.setText("Matrix Dimensions are from 1x1 to 10x10")
        self.info_label.adjustSize()
        self.choose_dimen_button = QPushButton()
        self.choose_dimen_button.setText("Choose Dimensions")

        # Dimensions Box
        self.sp1 = QSpinBox()
        self.sp1.setValue(4)
        self.sp1.setMaximum(10)
        self.sp1.setMinimum(1)
        self.label_x = QLabel()
        self.label_x.setAlignment(QtCore.Qt.AlignCenter)
        self.label_x.setText("X")
        self.sp2 = QSpinBox()
        self.sp2.setValue(4)
        self.sp2.setMaximum(10)
        self.sp2.setMinimum(1)

        # QFormLayout add row https://stackoverflow.com/questions/49582206/how-to-initialize-layouts-in-a-packed-way-reducing-space-between-layouts
        form = QFormLayout()
        dim_row_widget = QWidget()
        dim_widget = QWidget()
        dim_layout = QHBoxLayout()
        dim_layout.addWidget(self.sp1)
        dim_layout.addWidget(self.label_x)
        dim_layout.addWidget(self.sp2)
        dim_widget.setLayout(dim_layout)
        form.addWidget(dim_widget)
        dim_row_widget.setLayout(form)

        # Stack SubmitMatrixBox
        submitMatrix_layout = QFormLayout()
        submitMatrix_layout.addWidget(name_label)
        submitMatrix_layout.addWidget(self.info_label)
        submitMatrix_layout.addWidget(dim_row_widget)
        submitMatrix_layout.addWidget(self.choose_dimen_button)
        self.setLayout(submitMatrix_layout)


class MatrixEntry(QtWidgets.QWidget):
    def __init__(self, name: str, m=4, n=4, parent=None):
        """Class for input matrix table

        Args:
            name -- name of the matrix table
            m -- initial row number of matrix table
            n -- initial column number of matrix table
            parent -- widget/window holding MatrixEntry

        """
        super().__init__(parent)
        self.matrix_name = name
        self._initUi(m, n, name)

    def _initUi(self, m, n, name):

        # Matrix Grid Widget
        self.matrix_grid_widget = QTableWidget()
        self.matrix_grid_widget.setRowCount(m)
        self.matrix_grid_widget.setColumnCount(n)

        # Matrix Widget
        self.matrix_label = QLabel(name)
        self.matrix_widget_layout = QVBoxLayout()
        self.matrix_widget_layout.addWidget(self.matrix_label)
        self.matrix_widget_layout.addWidget(self.matrix_grid_widget)

        # Combine label and matrix grid
        self.setLayout(self.matrix_widget_layout)

    def resize_self(self, m: int, n: int):
        """Resizes input matrix (QTableWidget) dimensions and clears all current entries in the matrix

        Args:
            m -- new row dimension
            n -- new column dimension
        """
        # Clear Widgets
        self.matrix_grid_widget.clear()
        # Resize
        self.matrix_grid_widget.setRowCount(m)
        self.matrix_grid_widget.setColumnCount(n)
        for i in range(m):
            for j in range(n):
                self.matrix_grid_widget.setItem(i, j, QTableWidgetItem(""))
        self.matrix_grid_widget.adjustSize()

    def randomize_self(self, row_size: int, col_size: int):
        """Resizes matrix_grid_widget and then fills it with random ints between 1, 100.
        Args:
            row_size -- new row dimension
            col_size -- new column dimension

        """
        self.resize_self(row_size, col_size)
        for row in range(row_size):
            for col in range(col_size):
                number = str(random.randint(0, 100))
                self.matrix_grid_widget.setItem(row, col, QTableWidgetItem(number))
        self.matrix_grid_widget.resizeColumnsToContents()

    def return_matrix(self) -> (List[List[float]], FailureMessage):
        """ Exports matrix_grid_widget values as a 2D list where list[row,col] corresponds to matrix_grid_widget.item(row,col)"""
        self.matrix_grid_widget.update()
        my_matrix = []
        for row in range(self.matrix_grid_widget.rowCount()):
            my_matrix.append([])
            for col in range(self.matrix_grid_widget.columnCount()):

                item = self.matrix_grid_widget.item(row, col)
                if item is None:
                    return (
                        [],
                        FailureMessage("Cannot Have Empty Matrix Values"),
                    )
                try:
                    value = float(item.text())
                    # https://stackoverflow.com/questions/7604966/maximum-and-minimum-values-for-ints
                    if value > sys.maxsize or value < -sys.maxsize - 1:
                        return (
                            [[]],
                            FailureMessage(
                                "All values must be between -sys.maxint -1 and sys.maxint"
                            ),
                        )
                except Exception as e:
                    return (
                        [[]],
                        FailureMessage(
                            self.matrix_name
                            + ":  Invalid Matrix Entry: "
                            + str(e)
                            + " -- Remember to press enter after entering your last digit into each matrix."
                        ),
                    )

                my_matrix[row].append(value)
        return my_matrix, None


def main():
    app = QtWidgets.QApplication(sys.argv)
    win = MatrixEntryPage()
    win.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
