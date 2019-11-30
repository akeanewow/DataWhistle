import inspect
import os
import sys
import unittest
HDIR = os.path.dirname(os.path.abspath(
            inspect.getfile(inspect.currentframe())))
PARENTDIR = os.path.dirname(HDIR)
sys.path.insert(0, PARENTDIR)
import datawhistle.bqchecks as dwbc


class TestDFChecks(unittest.TestCase):

    def test_bqcheck_row_count(self):
        passed, message = dwbc.bqcheck_row_count('datawhistle', 'table1',
                                                 5, '>=')
        self.assertEqual(passed, True)
        self.assertEqual(message, '')


if __name__ == '__main__':
    unittest.main()
