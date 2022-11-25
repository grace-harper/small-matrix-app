"""small_matrix_app.matrix_app.tests.matrix_entry.test
Tests for Matrix Entry
"""
import random
import string
import sys

sys.path.insert(0, "..")

from PyQt5 import QtCore
from PyQt5.QtTest import QTest
import numpy as np
from PyQt5.QtWidgets import QApplication
import unittest

from matrix_app.db_widget import DisplayData, DatabaseModel, RunData
from matrix_app.matrix_entry_widget import MatrixEntryPage


class TestMatrixEntry(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.app = QApplication(sys.argv)

        letters = string.ascii_lowercase
        result_str = "".join(random.choice(letters) for i in range(12))
        cls.run_name = "TestRun" + result_str

        cls.A = DisplayData("A", np.array([[1, 2, 3], [1, 2, 3], [1, 2, 3]]))
        cls.B = DisplayData("B", np.array([[5, 10], [5, 10], [10, 10]]))
        cls.C = DisplayData("C", cls.A.data.dot(cls.B.data))

        cls.mep = MatrixEntryPage()

    def test_generate_random_matrix_displays(self) -> None:
        # check if each item in table has an int and that they can multiple
        self.mep._create_random_matrix()
        QTest.mouseClick(self.mep.generate_random_matrix_button, QtCore.Qt.LeftButton)
        left_table = self.mep.matrix_entry_left
        right_table = self.mep.matrix_entry_right
        left_size = (
            left_table.matrix_grid_widget.rowCount(),
            left_table.matrix_grid_widget.columnCount(),
        )
        right_size = (
            right_table.matrix_grid_widget.rowCount(),
            right_table.matrix_grid_widget.columnCount(),
        )

        assert left_size[1] == right_size[0]
        for r in range(left_size[0]):
            for c in range(left_size[1]):
                item = left_table.matrix_grid_widget.item(r, c)
                value = float(item.text())
                assert isinstance(value, float)

        for r in range(right_size[0]):
            for c in range(right_size[1]):
                item = right_table.matrix_grid_widget.item(r, c)
                value = float(item.text())
                assert isinstance(value, float)

        assert not right_table.matrix_grid_widget.isHidden()
        assert not left_table.matrix_grid_widget.isHidden()

    @classmethod
    def tearDownClass(cls):
        cls.mep.close()
        cls.mep = None
        cls.app.quit()
        cls.app = None


if __name__ == "__main__":
    unittest.main()
