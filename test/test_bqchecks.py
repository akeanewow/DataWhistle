import inspect
import os
import sys
import unittest
HDIR = os.path.dirname(os.path.abspath(
            inspect.getfile(inspect.currentframe())))
PARENTDIR = os.path.dirname(HDIR)
sys.path.insert(0, PARENTDIR)
import datawhistle.bqchecks as dwbc  # noqa


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
        # operator flag error
        passed, message = dwbc.dscheck_row_count('datawhistle', 'table1',
                                                 5, 'x=')
        self.assertFalse(passed)
        self.assertEqual(message,
                         'dataset row count operator x= not recognised')

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
        # operator incorrect
        passed, message = dwbc.colcheck_count_distinct('datawhistle', 'table1',
                                                       'A', 5, 'x=')
        self.assertFalse(passed)
        self.assertEqual(message,
                         'column A count distinct operator x= not recognised')

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

    def test_colcheck_iqr(self):
        passed, message = dwbc.colcheck_iqr('datawhistle', 'table1', 'A')
        self.assertTrue(passed)
        self.assertEqual(message, '')
        passed, message = dwbc.colcheck_iqr('datawhistle', 'table2', 'B')
        self.assertFalse(passed)
        self.assertEqual(message, 'column B want 0 outliers, got 1.0')

    def test_colcheck_is_datetime(self):
        passed, message = dwbc.colcheck_is_datetime('datawhistle', 'table1',
                                                    'J')
        self.assertTrue(passed)
        self.assertEqual(message, '')
        passed, message = dwbc.colcheck_is_datetime('datawhistle', 'table1',
                                                    'K')
        self.assertFalse(passed)
        self.assertEqual(message, 'column K want datetime type, got STRING')

    def test_colcheck_no_blanks(self):
        passed, message = dwbc.colcheck_no_blanks('datawhistle', 'table1',
                                                  'C')
        self.assertTrue(passed)
        self.assertEqual(message, '')
        passed, message = dwbc.colcheck_no_blanks('datawhistle', 'table2',
                                                  'G')
        self.assertFalse(passed)
        self.assertEqual(message, 'column G want no blanks, got 1.0')

    def test_colcheck_no_duplicates(self):
        passed, message = dwbc.colcheck_no_duplicates('datawhistle', 'table1',
                                                      'A')
        self.assertTrue(passed)
        self.assertEqual(message, '')
        passed, message = dwbc.colcheck_no_duplicates('datawhistle', 'table2',
                                                      'A')
        self.assertFalse(passed)
        self.assertEqual(message, 'column A want 0 duplicate rows, got 2.0')

    def test_colcheck_no_nulls(self):
        passed, message = dwbc.colcheck_no_nulls('datawhistle', 'table1', 'A')
        self.assertTrue(passed)
        self.assertEqual(message, '')
        passed, message = dwbc.colcheck_no_nulls('datawhistle', 'table1', 'D')
        self.assertFalse(passed)
        self.assertEqual(message, 'column D want 0 nulls, got 2.0')

    def test_colcheck_regex(self):
        # Fails
        passed, message = dwbc.colcheck_regex('datawhistle', 'table1', 'C',
                                              '', 'mandatory')
        self.assertFalse(passed)
        self.assertEqual(message, 'column C blank regex_rule')
        passed, message = dwbc.colcheck_regex('datawhistle', 'table1', 'C',
                                              '[', 'mandatory')
        self.assertFalse(passed)
        self.assertEqual(message, 'column C BqError with rule [')
        passed, message = dwbc.colcheck_regex('datawhistle', 'table1', 'C',
                                              '[a]', 'mandatory')
        self.assertFalse(passed)
        self.assertEqual(
            message,
            'column C found a non matching regex record with rule [a]')
        passed, message = dwbc.colcheck_regex('datawhistle', 'table1', 'C',
                                              '[b]', 'exclude')
        self.assertFalse(passed)
        self.assertEqual(message, 'column C found invalid regex with rule [b]')
        # Succeeds
        passed, message = dwbc.colcheck_regex('datawhistle', 'table1', 'C',
                                              '[z]', 'exclude')
        self.assertTrue(passed)
        self.assertEqual(message, '')
        passed, message = dwbc.colcheck_regex('datawhistle', 'table1', 'C',
                                              '.', 'mandatory')
        self.assertTrue(passed)
        self.assertEqual(message, '')

    def test_col_val(self):
        # >= checks
        passed, message = dwbc.colcheck_val('datawhistle', 'table1', 'A',
                                            -1, '>=')
        self.assertTrue(passed)
        self.assertEqual(message, '')
        passed, message = dwbc.colcheck_val('datawhistle', 'table1', 'A',
                                            2, '>=')
        self.assertFalse(passed)
        self.assertEqual(message, 'column A want value >= 2, got 1.0')
        # <= checks
        passed, message = dwbc.colcheck_val('datawhistle', 'table1', 'A',
                                            5, '<=')
        self.assertTrue(passed)
        self.assertEqual(message, '')
        passed, message = dwbc.colcheck_val('datawhistle', 'table1', 'A',
                                            2, '<=')
        self.assertFalse(passed)
        self.assertEqual(message, 'column A want value <= 2, got 5.0')
        # == checks
        passed, message = dwbc.colcheck_val('datawhistle', 'table1', 'I',
                                            1, '==')
        self.assertTrue(passed)
        self.assertEqual(message, '')
        passed, message = dwbc.colcheck_val('datawhistle', 'table1', 'A',
                                            1, '==')
        self.assertFalse(passed)
        self.assertEqual(message, 'column A want value == 1, got 4.0 not')
        # operator incorrect
        passed, message = dwbc.colcheck_val('datawhistle', 'table1', 'I',
                                            1, 'x=')
        self.assertFalse(passed)
        self.assertEqual(message,
                         'column I value check operator x= not recognised')


if __name__ == '__main__':
    unittest.main()
