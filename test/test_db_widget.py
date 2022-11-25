"""small_matrix_app.matrix_app.tests.db_widget_test.py
Tests for Database Widget Class
"""
import sys

sys.path.insert(0, "..")
import unittest

import os
import random
import string
import numpy as np
from PyQt5.QtWidgets import QApplication

from matrix_app.all_exceptions import CriticalFailure, FailureMessage
from matrix_app.db_widget import DatabaseModel, DisplayData, RunData


class TestDbWidget(unittest.TestCase):
    """Test db_widget"""

    @classmethod
    def setUpClass(cls):
        """Setup for DB Interface tests"""
        cls.app = QApplication(sys.argv)
        cls.db_dir = os.getcwd() + "DbDir"
        if not os.path.exists(cls.db_dir):
            os.mkdir(cls.db_dir)

    def setUp(self):
        letters = string.ascii_lowercase
        result_str = "".join(random.choice(letters) for i in range(12))
        self.db_name = self.db_dir + "/" + result_str
        self.run_name = "TestRun" + result_str
        self.A = DisplayData("A", np.array([[1, 2, 3], [1, 2, 3], [1, 2, 3]]))
        self.B = DisplayData("B", np.array([[5, 10], [5, 10], [10, 10]]))
        self.C = DisplayData("C", self.A.data.dot(self.B.data))

        s1 = DisplayData("all cumprod", self.C.data.cumprod())
        # manually checked in termial this is column
        s2 = DisplayData("col cumprod", self.C.data.cumprod(axis=0))
        s3 = DisplayData("row min", self.C.data.min(axis=1))

        self.run_data = RunData(self.run_name, [self.A, self.B, self.C], [s1, s2, s3])
        self.db = None

    def test_setup_db_preexisting_file(self):
        """Tests failing db on a preexisting db-named file """
        with self.assertRaises(CriticalFailure) as cf:
            with open(self.db_name, "w+") as f:
                pass
            self.db = DatabaseModel(self.db_name)
            self.db.close()
            self.db = None

        assert "Critical Failure" in str(cf.exception)
        os.remove(self.db_name)

    def test_save_run_pre_existing_file(self):
        """Tests saving run with same name as pre-existing run"""
        self.db = DatabaseModel(self.db_name)
        assert self.db is not None

        run_name_file = self.run_name + ".h5"
        with open(self.db_name + "/" + run_name_file, "w+") as f:
            f.write("fish")
        fm = self.db.save_run(self.run_data)
        self.db.close()
        self.db = None
        assert isinstance(fm, FailureMessage)

    @classmethod
    def tearDownClass(self):
        self.db = None
        self.app.quit()
        self.app = None


def suite():
    """
    Gather all the tests from this module in a test suite.
    """
    test_suite = unittest.TestSuite()
    test_suite.addTest(unittest.makeSuite(TestDbWidget))
    return test_suite


if __name__ == "__main__":
    unittest.main()
