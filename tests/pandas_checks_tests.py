import pandas_checks as pc
import unittest
import sys
sys.path.append('../src')
import pandas as pd  # noqa: e402


class TestDFChecks(unittest.TestCase):

    def setUp(self):
        self.df_file1 = pd.read_csv('data/file1.csv')
        self.df_file2 = pd.read_csv('data/file2.csv')

    def test_min_rows(self):
        passed, message = pc.dfcheck_min_rows(self.df_file1, 5)
        self.assertEqual(passed, True)
        self.assertEqual(message, '')
        passed, message = pc.dfcheck_min_rows(self.df_file1, 10)
        self.assertEqual(passed, False)
        self.assertEqual(message, 'want 10 rows, got 5')

    def test_no_duplicate_rows(self):
        passed, message = pc.dfcheck_no_duplicate_rows(self.df_file1)
        self.assertEqual(passed, True)
        self.assertEqual(message, '')
        passed, message = pc.dfcheck_no_duplicate_rows(self.df_file2)
        self.assertEqual(passed, False)
        self.assertEqual(message, 'want 0 duplicate rows, got 2')


class TestColChecks(unittest.TestCase):

    def setUp(self):
        self.df_file1 = pd.read_csv('data/file1.csv')

    def test_col_exists(self):
        passed, message = pc.colcheck_col_exists(self.df_file1, 'x')
        self.assertEqual(passed, False)
        self.assertEqual(message, 'column x not found in data')
        passed, message = pc.colcheck_col_exists(self.df_file1, 'A')
        self.assertEqual(passed, True)
        self.assertEqual(message, '')

    def test_col_is_numeric(self):
        passed, message = pc.colcheck_is_numeric(self.df_file1, 'C')
        self.assertEqual(passed, False)
        self.assertEqual(message, 'column C expected to be numeric but is not')
        passed, message = pc.colcheck_is_numeric(self.df_file1, 'A')
        self.assertEqual(passed, True)
        self.assertEqual(message, '')

    def test_col_is_str(self):
        passed, message = pc.colcheck_is_str(self.df_file1, 'A')
        self.assertEqual(passed, False)
        self.assertEqual(
                message,
                'column A expected to be string type but is not')
        passed, message = pc.colcheck_is_str(self.df_file1, 'C')
        self.assertEqual(passed, True)

    def test_min_val(self):
        passed, message = pc.colcheck_min_val(self.df_file1, 'A', -1)
        self.assertEqual(passed, True)
        self.assertEqual(message, '')
        passed, message = pc.colcheck_min_val(self.df_file1, 'A', 2)
        self.assertEqual(passed, False)
        self.assertEqual(message, 'column A want 2 minimum value, got 1')


if __name__ == '__main__':
    unittest.main()
