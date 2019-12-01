import inspect
import os
import sys
import unittest
HDIR = os.path.dirname(os.path.abspath(
            inspect.getfile(inspect.currentframe())))
PARENTDIR = os.path.dirname(HDIR)
sys.path.insert(0, PARENTDIR)
import datawhistle.bqchecks as dwbc


class TestTableLevelChecks(unittest.TestCase):

    def test_dscheck_row_count(self):
        # >=
        passed, message = dwbc.dscheck_row_count('datawhistle', 'table1',
                                                 5, '>=')
        self.assertTrue(passed)
        self.assertEqual(message, '')
        passed, message = dwbc.dscheck_row_count('datawhistle', 'table1',
                                                 10, '>=')
        self.assertFalse(passed)
        self.assertEqual(message, 'want row count >= 10, got 5.0')
        # <=
        passed, message = dwbc.dscheck_row_count('datawhistle', 'table1',
                                                 10, '<=')
        self.assertTrue(passed)
        self.assertEqual(message, '')
        passed, message = dwbc.dscheck_row_count('datawhistle', 'table1',
                                                 2, '<=')
        self.assertFalse(passed)
        self.assertEqual(message, 'want row count <= 2, got 5.0')
        # ==
        passed, message = dwbc.dscheck_row_count('datawhistle', 'table1',
                                                 5, '==')
        self.assertTrue(passed)
        self.assertEqual(message, '')
        passed, message = dwbc.dscheck_row_count('datawhistle', 'table1',
                                                 10, '==')
        self.assertFalse(passed)
        self.assertEqual(message, 'want row count == 10, got 5.0')

    def test_dscheck_table_exists(self):
        passed, message = dwbc.dscheck_table_exists('datawhistle', 'table1')
        self.assertTrue(passed)
        self.assertEqual(message, '')
        passed, message = dwbc.dscheck_table_exists('datawhistle', 'zzz')
        self.assertFalse(passed)
        self.assertEqual(message, 'table zzz not found in dataset datawhistle')


class TestColumnLevelChecks(unittest.TestCase):

    def test_colcheck_exists(self):
        passed, message = dwbc.colcheck_exists('datawhistle', 'table1', 'A')
        self.assertTrue(passed)
        self.assertEqual(message, '')
        passed, message = dwbc.colcheck_exists('datawhistle', 'table1', 'XX')
        self.assertFalse(passed)
        self.assertEqual(message, 'column XX not found in table table1')


if __name__ == '__main__':
    unittest.main()
