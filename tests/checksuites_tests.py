import sys
sys.path.append('../src')
import checksuites as cs
import unittest
import pandas as pd


class TestPandasDatasetCheckSuite(unittest.TestCase):

    def setUp(self):
        self.df_file1 = pd.read_csv('data/file1.csv')
        self.df_file2 = pd.read_csv('data/file2.csv')

    def test_run_checks_datsetobjectonly(self):
        pdcs = cs.PandasDatsetCheckSuite(self.df_file1)
        pdcs.run_checks()
        self.assertEqual(len(pdcs.error_messages), 0)
        pdcs.allow_duplicate_rows = False
        pdcs.run_checks()
        self.assertEqual(len(pdcs.error_messages), 0)
        pdcs = cs.PandasDatsetCheckSuite(self.df_file2)
        pdcs.run_checks()
        self.assertEqual(len(pdcs.error_messages), 0)
        pdcs.allow_duplicate_rows = False
        pdcs.run_checks()
        self.assertEqual(len(pdcs.error_messages), 1)
        self.assertEqual(pdcs.error_messages, ['want 0 duplicate rows, got 2'])

    def test_run_checks_columnobjectonly(self):
        pdcs = cs.PandasColumnCheckSuite(self.df_file1, 'A', 'numeric')
        pdcs.run_checks(False)
        self.assertEqual(len(pdcs.error_messages), 0)
        pdcs = cs.PandasColumnCheckSuite(self.df_file1, 'C', 'numeric')
        pdcs.run_checks(False)
        self.assertEqual(len(pdcs.error_messages), 1)
        self.assertEqual(pdcs.error_messages, ['column C expected to be numeric but is not'])


if __name__ == '__main__':
    unittest.main()
