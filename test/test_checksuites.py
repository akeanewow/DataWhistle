import inspect
import os
import sys
import unittest
HDIR = os.path.dirname(os.path.abspath(
            inspect.getfile(inspect.currentframe())))
PARENTDIR = os.path.dirname(HDIR)
sys.path.insert(0, PARENTDIR)
import pandas as pd  # type: ignore
import datawhistle as dw  # noqa


class TestPandasTableCheckSuite(unittest.TestCase):

    def setUp(self):
        self.df_file1 = pd.read_csv(os.path.join(HDIR, 'data/file1.csv'))
        self.df_file2 = pd.read_csv(os.path.join(HDIR, 'data/file2.csv'))

    def test_runchecks_datasetobjectonly(self):
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
        pdcs = dw.PandasColumnCheckSuite(self.df_file2, 'B', 'numeric')
        pdcs.runchecks(False)


class TestBqTableCheckSuite(unittest.TestCase):

    def test_runchecks_tableobject_only(self):
        bqts = dw.BqTableCheckSuite('datawhistle', 'table1')
        bqts.runchecks()
        self.assertEqual(len(bqts.error_messages), 0)

    def test_runchecks_columnobjectonly(self):
        # numeric type
        bqcs = dw.BqColumnCheckSuite('datawhistle', 'table1', 'A', 'numeric')
        bqcs.runchecks(False)
        self.assertEqual(len(bqcs.error_messages), 0)
        bqcs = dw.BqColumnCheckSuite('datawhistle', 'table1', 'C', 'numeric')
        bqcs.runchecks(False)
        self.assertEqual(
                bqcs.error_messages,
                ['column C want numeric type, got STRING'])
        bqcs = dw.BqColumnCheckSuite('datawhistle', 'table1', 'X', 'numeric')
        bqcs.runchecks(False)
        self.assertEqual(bqcs.error_messages,
                         ['column X not found in table table1'])
        # string type
        bqcs = dw.BqColumnCheckSuite('datawhistle', 'table1', 'C', 'string')
        bqcs.runchecks(False)
        self.assertEqual(len(bqcs.error_messages), 0)
        bqcs = dw.BqColumnCheckSuite('datawhistle', 'table1', 'A', 'string')
        bqcs.runchecks(False)
        self.assertEqual(
                bqcs.error_messages,
                ['column A want string type, got INT64'])
        bqcs = dw.BqColumnCheckSuite('datawhistle', 'table1', 'B', 'numeric')
        bqcs.runchecks(False)


if __name__ == '__main__':
    unittest.main()
