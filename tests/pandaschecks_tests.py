import unittest
import pandas as pd  # type: ignore
import sys
sys.path.append('..')
import datawhistle.pandaschecks as dwpc


class TestDFChecks(unittest.TestCase):

    def setUp(self):
        self.df_file1 = pd.read_csv('data/file1.csv')
        self.df_file2 = pd.read_csv('data/file2.csv')

    def test_row_count(self):
        passed, message = dwpc.dfcheck_row_count(self.df_file1, 5, '>=')
        self.assertEqual(passed, True)
        self.assertEqual(message, '')
        passed, message = dwpc.dfcheck_row_count(self.df_file1, 10, '>=')
        self.assertEqual(passed, False)
        self.assertEqual(message, 'want row count >= 10, got 5')

    def test_no_duplicate_rows(self):
        passed, message = dwpc.dfcheck_no_duplicate_rows(self.df_file1)
        self.assertEqual(passed, True)
        self.assertEqual(message, '')
        passed, message = dwpc.dfcheck_no_duplicate_rows(self.df_file2)
        self.assertEqual(passed, False)
        self.assertEqual(message, 'want 0 duplicate rows, got 2')


class TestColChecks(unittest.TestCase):

    def setUp(self):
        self.df_file1 = pd.read_csv('data/file1.csv')
        self.df_file2 = pd.read_csv('data/file2.csv')

    def test_col_exists(self):
        passed, message = dwpc.colcheck_exists(self.df_file1, 'x')
        self.assertEqual(passed, False)
        self.assertEqual(message, 'column x not found in data')
        passed, message = dwpc.colcheck_exists(self.df_file1, 'A')
        self.assertEqual(passed, True)
        self.assertEqual(message, '')

    def test_col_count_distinct(self):
        passed, message = dwpc.colcheck_count_distinct(self.df_file1,
                                                       'G', 3, '>=')
        self.assertEqual(passed, False)
        self.assertEqual(message, 'column G want count distinct >= 3, got 2')
        passed, message = dwpc.colcheck_count_distinct(self.df_file1,
                                                       'G', 1, '<=')
        self.assertEqual(passed, False)
        self.assertEqual(message, 'column G want count distinct <= 1, got 2')
        passed, message = dwpc.colcheck_count_distinct(self.df_file1, 'G', 2)
        self.assertEqual(passed, True)
        passed, message = dwpc.colcheck_count_distinct(self.df_file1, 'A', 5)
        self.assertEqual(passed, True)

    def test_col_is_numeric(self):
        passed, message = dwpc.colcheck_is_numeric(self.df_file1, 'C')
        self.assertEqual(passed, False)
        self.assertEqual(message, 'column C expected to be numeric but is not')
        passed, message = dwpc.colcheck_is_numeric(self.df_file1, 'A')
        self.assertEqual(passed, True)
        self.assertEqual(message, '')

    def test_col_is_str(self):
        passed, message = dwpc.colcheck_is_str(self.df_file1, 'A')
        self.assertEqual(passed, False)
        self.assertEqual(
                message,
                'column A expected to be string type but is not')
        passed, message = dwpc.colcheck_is_str(self.df_file1, 'C')
        self.assertEqual(passed, True)

    def test_min_val(self):
        passed, message = dwpc.colcheck_min_val(self.df_file1, 'A', -1)
        self.assertEqual(passed, True)
        self.assertEqual(message, '')
        passed, message = dwpc.colcheck_min_val(self.df_file1, 'A', 2)
        self.assertEqual(passed, False)
        self.assertEqual(message, 'column A want 2 minimum value, got 1')

    def test_col_no_blanks(self):
        passed, message = dwpc.colcheck_no_blanks(self.df_file1, 'H')
        self.assertEqual(passed, True)
        self.assertEqual(message, '')
        passed, message = dwpc.colcheck_no_blanks(self.df_file2, 'G')
        self.assertEqual(passed, False)
        self.assertEqual(message, 'column G has blanks or whitesplace only values')


    def test_col_no_nulls(self):
        passed, message = dwpc.colcheck_no_nulls(self.df_file1, 'A')
        self.assertEqual(passed, True)
        self.assertEqual(message, '')
        passed, message = dwpc.colcheck_no_nulls(self.df_file1, 'D')
        self.assertEqual(passed, False)
        self.assertEqual(message, 'column D want 0 nulls, got 2')


if __name__ == '__main__':
    unittest.main()
