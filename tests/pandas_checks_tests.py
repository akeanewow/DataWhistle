import sys
sys.path.append('../src')
import pandas_checks as pc
import unittest
import pandas as pd

class TestDFChecks(unittest.TestCase):

    def setUp(self):
        self.df_file1 = pd.read_csv('data/file1.csv')

    def test_min_rows(self):
        passed, message = pc.dfcheck_min_rows(self.df_file1, 5)
        self.assertEqual(passed, True)
        self.assertEqual(message, '')
        passed, message = pc.dfcheck_min_rows(self.df_file1, 10)
        self.assertEqual(passed, False)
        self.assertEqual(message, 'want 10 rows, got 5')

if __name__ == '__main__':
    unittest.main()
