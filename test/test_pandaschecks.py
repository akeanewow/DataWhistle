import inspect
import os
import sys
import unittest
HDIR = os.path.dirname(os.path.abspath(
            inspect.getfile(inspect.currentframe())))
PARENTDIR = os.path.dirname(HDIR)
sys.path.insert(0, PARENTDIR)
import pandas as pd     # type: ignore
import datawhistle.pandaschecks as dwpc  # noqa


class TestDFChecks(unittest.TestCase):

    def setUp(self):
        self.df_file1 = pd.read_csv(os.path.join(HDIR, 'data/file1.csv'))
        self.df_file2 = pd.read_csv(os.path.join(HDIR, 'data/file2.csv'))

    def test_row_count(self):
        passed, message = dwpc.dfcheck_row_count(self.df_file1, 5, '>=')
        self.assertTrue(passed)
        self.assertEqual(message, '')
        passed, message = dwpc.dfcheck_row_count(self.df_file1, 10, '>=')
        self.assertFalse(passed)
        self.assertEqual(message, 'want row count >= 10, got 5')

    def test_no_duplicate_rows(self):
        passed, message = dwpc.dfcheck_no_duplicate_rows(self.df_file1)
        self.assertTrue(passed)
        self.assertEqual(message, '')
        passed, message = dwpc.dfcheck_no_duplicate_rows(self.df_file2)
        self.assertFalse(passed)
        self.assertEqual(message, 'want 0 duplicate rows, got 2')


class TestColChecks(unittest.TestCase):

    def setUp(self):
        self.df_file1 = pd.read_csv(os.path.join(HDIR, 'data/file1.csv'))
        self.df_file2 = pd.read_csv(os.path.join(HDIR, 'data/file2.csv'))

    def test_col_exists(self):
        passed, message = dwpc.colcheck_exists(self.df_file1, 'x')
        self.assertFalse(passed)
        self.assertEqual(message, 'column x not found in data')
        passed, message = dwpc.colcheck_exists(self.df_file1, 'A')
        self.assertTrue(passed)
        self.assertEqual(message, '')

    def test_col_count_distinct(self):
        passed, message = dwpc.colcheck_count_distinct(self.df_file1,
                                                       'G', 3, '>=')
        self.assertFalse(passed)
        self.assertEqual(message, 'column G want count distinct >= 3, got 2')
        passed, message = dwpc.colcheck_count_distinct(self.df_file1,
                                                       'G', 1, '<=')
        self.assertFalse(passed)
        self.assertEqual(message, 'column G want count distinct <= 1, got 2')
        passed, message = dwpc.colcheck_count_distinct(self.df_file1, 'G', 2)
        self.assertTrue(passed)
        passed, message = dwpc.colcheck_count_distinct(self.df_file1, 'A', 5)
        self.assertTrue(passed)

    def test_col_is_numeric(self):
        passed, message = dwpc.colcheck_is_numeric(self.df_file1, 'C')
        self.assertFalse(passed)
        self.assertEqual(message, 'column C expected to be numeric but is not')
        passed, message = dwpc.colcheck_is_numeric(self.df_file1, 'A')
        self.assertTrue(passed)
        self.assertEqual(message, '')

    def test_col_is_str(self):
        passed, message = dwpc.colcheck_is_str(self.df_file1, 'A')
        self.assertFalse(passed)
        self.assertEqual(
                message,
                'column A expected to be string type but is not')
        passed, message = dwpc.colcheck_is_str(self.df_file1, 'C')
        self.assertTrue(passed)

    def test_col_no_blanks(self):
        passed, message = dwpc.colcheck_no_blanks(self.df_file1, 'H')
        self.assertTrue(passed)
        self.assertEqual(message, '')
        passed, message = dwpc.colcheck_no_blanks(self.df_file2, 'G')
        self.assertFalse(passed)
        self.assertEqual(
                message,
                'column G has blanks or whitesplace only values')

    def test_col_is_datetime(self):
        passed, message = dwpc.colcheck_is_datetime(self.df_file1, 'K',
                                                    '%m/%d/%Y')
        self.assertEqual(passed, False)
        self.assertEqual(
            message,
            'column K data does not match datetime format %m/%d/%Y')
        passed, message = dwpc.colcheck_is_datetime(self.df_file1, 'K')
        self.assertEqual(passed, False)
        self.assertEqual(
            message,
            'column K expected to be datetime type but is not')
        passed, message = dwpc.colcheck_is_datetime(self.df_file1, 'J')
        self.assertEqual(passed, True)
        passed, message = dwpc.colcheck_is_datetime(self.df_file1, 'J',
                                                    '%m/%d/%Y')
        self.assertEqual(passed, True)

    def test_col_regex(self):
        #Fails
        passed, message = dwpc.colcheck_regex(self.df_file1, 'C', '', 'mandatory')
        self.assertEqual(passed, False)
        self.assertEqual(
            message,
            'column C blank regex_rule')
        passed, message = dwpc.colcheck_regex(self.df_file1, 'C', '[', 'mandatory')
        self.assertEqual(passed, False)
        self.assertEqual(
            message,
            'column C invalid regex_rule [')
        passed, message = dwpc.colcheck_regex(self.df_file1, 'C', '[a]', 'mandatory')
        self.assertEqual(passed, False)
        self.assertEqual(
            message,
            'column C found a non matching regex record with rule [a]')
        passed, message = dwpc.colcheck_regex(self.df_file1, 'C', '[b]', 'exclude')
        self.assertEqual(passed, False)
        self.assertEqual(
            message,
            'column C found invalid regex b with rule [b]')
        #Succeds
        passed, message = dwpc.colcheck_regex(self.df_file1, 'C', '[z]', 'exclude')
        self.assertEqual(passed, True)
        self.assertEqual(
            message,
            '')
        passed, message = dwpc.colcheck_regex(self.df_file1, 'C', '.', 'mandatory')
        self.assertEqual(passed, True)
        self.assertEqual(
            message,
            '')

    def test_col_no_duplicates(self):
        passed, message = dwpc.colcheck_no_duplicates(self.df_file1, 'I')
        self.assertFalse(passed)
        self.assertEqual(message, 'column I want 0 duplicate rows, got 4')
        passed, message = dwpc.colcheck_no_duplicates(self.df_file1, 'A')
        self.assertTrue(passed)
        self.assertEqual(message, '')

    def test_col_no_nulls(self):
        passed, message = dwpc.colcheck_no_nulls(self.df_file1, 'A')
        self.assertTrue(passed)
        self.assertEqual(message, '')
        passed, message = dwpc.colcheck_no_nulls(self.df_file1, 'D')
        self.assertFalse(passed)
        self.assertEqual(message, 'column D want 0 nulls, got 2')

    def test_col_val(self):
        # >= checks
        passed, message = dwpc.colcheck_val(self.df_file1, 'A', -1, '>=')
        self.assertTrue(passed)
        self.assertEqual(message, '')
        passed, message = dwpc.colcheck_val(self.df_file1, 'A', 2, '>=')
        self.assertFalse(passed)
        self.assertEqual(message, 'column A want value >= 2, got 1')
        # <= checks
        passed, message = dwpc.colcheck_val(self.df_file1, 'A', 5, '<=')
        self.assertTrue(passed)
        self.assertEqual(message, '')
        passed, message = dwpc.colcheck_val(self.df_file1, 'A', 2, '<=')
        self.assertFalse(passed)
        self.assertEqual(message, 'column A want value <= 2, got 5')
        # == checks
        passed, message = dwpc.colcheck_val(self.df_file1, 'I', 1, '==')
        self.assertTrue(passed)
        self.assertEqual(message, '')
        passed, message = dwpc.colcheck_val(self.df_file1, 'A', 1, '==')
        self.assertFalse(passed)
        self.assertEqual(message, (f'column A want all values = 1,'
                                   ' got different values'))

    def test_col_iqr(self):
        passed, message = dwpc.colcheck_iqr(self.df_file2, 'A')
        self.assertTrue(passed)
        self.assertEqual(message, '')
        passed, message = dwpc.colcheck_iqr(self.df_file2, 'B')
        self.assertFalse(passed)
        self.assertEqual(message, 'column B outlier above 1.5xIQR 10.35: 12.1')


if __name__ == '__main__':
    unittest.main()
