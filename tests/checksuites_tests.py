import unittest
import pandas as pd  # type: ignore
import sys
sys.path.append('..')
import datawhistle as dw


class TestPandasDatasetCheckSuite(unittest.TestCase):

    def setUp(self):
        self.df_file1 = pd.read_csv('data/file1.csv')
        self.df_file2 = pd.read_csv('data/file2.csv')

    def test_runchecks_datsetobjectonly(self):
        pdcs = dw.PandasDatsetCheckSuite(self.df_file1)
        pdcs.runchecks()
        self.assertEqual(len(pdcs.error_messages), 0)
        pdcs.allow_duplicate_rows = False
        pdcs.runchecks()
        self.assertEqual(len(pdcs.error_messages), 0)
        pdcs = dw.PandasDatsetCheckSuite(self.df_file2)
        pdcs.runchecks()
        self.assertEqual(len(pdcs.error_messages), 0)
        pdcs.allow_duplicate_rows = False
        pdcs.runchecks()
        self.assertEqual(pdcs.error_messages, ['want 0 duplicate rows, got 2'])

    def test_runchecks_columnobjectonly(self):
        # numeric type
        pdcs = dw.PandasColumnCheckSuite(self.df_file1, 'A', 'numeric')
        pdcs.runchecks(False)
        self.assertEqual(len(pdcs.error_messages), 0)
        pdcs = dw.PandasColumnCheckSuite(self.df_file1, 'C', 'numeric')
        pdcs.runchecks(False)
        self.assertEqual(
                pdcs.error_messages,
                ['column C expected to be numeric but is not'])
        pdcs = dw.PandasColumnCheckSuite(self.df_file1, 'X', 'numeric')
        pdcs.runchecks(False)
        self.assertEqual(pdcs.error_messages, ['column X not found in data'])
        # string type
        pdcs = dw.PandasColumnCheckSuite(self.df_file1, 'C', 'string')
        pdcs.runchecks(False)
        self.assertEqual(len(pdcs.error_messages), 0)
        pdcs = dw.PandasColumnCheckSuite(self.df_file1, 'A', 'string')
        pdcs.runchecks(False)
        self.assertEqual(
                pdcs.error_messages,
                ['column A expected to be string type but is not'])


if __name__ == '__main__':
    unittest.main()
