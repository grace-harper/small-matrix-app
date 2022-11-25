import sys
import unittest
import matrix_app.test.test_db_widget as dbtest
from PyQt5.QtWidgets import QApplication

qApp = None

if __name__ == "__main__":
    qApp = QApplication(sys.argv)
    testSuite = unittest.TestSuite()
    testSuite.addTest(dbtest.suite())
    testResult = unittest.TestResult()
    tests = testSuite.run(testResult)

    print(testResult.testsRun)
