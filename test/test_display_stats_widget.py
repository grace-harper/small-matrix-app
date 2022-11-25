"""small_matrix_app.matrix_app.tests..display_stats_test.py
Tests for Display Stats Class
"""

import string
import sys

sys.path.insert(0, "..")
import random

import unittest
from PyQt5 import QtCore
from PyQt5.QtTest import QTest
import numpy as np
from PyQt5.QtWidgets import QApplication

# noinspection PyInterpreter
from matrix_app.db_widget import DisplayData, DatabaseModel, RunData
from matrix_app.display_stats_widget import DisplayStatsPage


class TestDisplayStats(unittest.TestCase):
    """Tests display_stats widget"""

    @classmethod
    def setUpClass(cls):
        """Set up for Display Stats tests"""

        cls.app = QApplication(sys.argv)

        letters = string.ascii_lowercase
        result_str = "".join(random.choice(letters) for i in range(12))
        cls.run_name = "TestRun" + result_str

        cls.A = DisplayData("A", np.array([[1, 2, 3], [1, 2, 3], [1, 2, 3]]))
        cls.B = DisplayData("B", np.array([[5, 10], [5, 10], [10, 10]]))
        cls.C = DisplayData("C", cls.A.data.dot(cls.B.data))

        s1 = DisplayData("all cumprod", cls.C.data.cumprod())
        # manually checked in termial this is column
        s2 = DisplayData("col cumprod", cls.C.data.cumprod(axis=0))
        s3 = DisplayData("row min", cls.C.data.min(axis=1))

        cls.run_data = RunData(cls.run_name, [cls.A, cls.B, cls.C], [s1, s2, s3])

        cls.dsp = DisplayStatsPage(run_data=cls.run_data)

    def test_calculate(self):
        """Test Calculate Stats"""
        QTest.mouseClick(self.dsp.calculate_current_stats_button, QtCore.Qt.LeftButton)
        assert self.dsp.data_display_layout.count() is not None
        assert self.dsp.calculate_current_stats_button.isHidden()

    @classmethod
    def tearDownClass(self):
        self.dsp.close()
        self.dsp = None
        self.app.quit()
        self.app = None


if __name__ == "__main__":
    unittest.main()
