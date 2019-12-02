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

    def test_colcheck_count_distinct(self):
        # >=
        passed, message = dwbc.colcheck_count_distinct('datawhistle', 'table1',
                                                       'A', 5, '>=')
        self.assertTrue(passed)
        self.assertEqual(message, '')
        passed, message = dwbc.colcheck_count_distinct('datawhistle', 'table1',
                                                       'A', 6, '>=')
        self.assertFalse(passed)
        self.assertEqual(message, ('column A want count distinct >= 6, '
                                   'got 5.0'))
        # <=
        passed, message = dwbc.colcheck_count_distinct('datawhistle', 'table1',
                                                       'A', 10, '<=')
        self.assertTrue(passed)
        self.assertEqual(message, '')
        passed, message = dwbc.colcheck_count_distinct('datawhistle', 'table1',
                                                       'A', 3, '<=')
        self.assertFalse(passed)
        self.assertEqual(message, ('column A want count distinct <= 3, '
                                   'got 5.0'))
        # ==
        passed, message = dwbc.colcheck_count_distinct('datawhistle', 'table1',
                                                       'A', 5, '==')
        self.assertTrue(passed)
        self.assertEqual(message, '')
        passed, message = dwbc.colcheck_count_distinct('datawhistle', 'table1',
                                                       'A', 6, '==')
        self.assertFalse(passed)
        self.assertEqual(message, ('column A want count distinct == 6, '
                                   'got 5.0'))

    def test_colcheck_is_numeric(self):
        passed, message = dwbc.colcheck_is_numeric('datawhistle', 'table1',
                                                   'A')
        self.assertTrue(passed)
        self.assertEqual(message, '')
        passed, message = dwbc.colcheck_is_numeric('datawhistle', 'table1',
                                                   'B')
        self.assertTrue(passed)
        self.assertEqual(message, '')
        passed, message = dwbc.colcheck_is_numeric('datawhistle', 'table1',
                                                   'C')
        self.assertFalse(passed)
        self.assertEqual(message, 'column C want numeric type, got STRING')

    def test_colcheck_is_str(self):
        passed, message = dwbc.colcheck_is_str('datawhistle', 'table1',
                                               'C')
        self.assertTrue(passed)
        self.assertEqual(message, '')
        passed, message = dwbc.colcheck_is_str('datawhistle', 'table1',
                                               'A')
        self.assertFalse(passed)
        self.assertEqual(message, 'column A want string type, got INT64')


if __name__ == '__main__':
    unittest.main()
