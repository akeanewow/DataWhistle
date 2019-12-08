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


class TestYamlParsing(unittest.TestCase):

    def setUp(self):
        filepath = os.path.join(HDIR, 'data/file1.csv')
        self.df_file1 = pd.read_csv(filepath)
        self.file1path = os.path.join(HDIR, 'yamls/file1.yaml')
        self.file2path = os.path.join(HDIR, 'yamls/file2.yaml')
        self.file3path = os.path.join(HDIR, 'yamls/file3.yaml')
        self.file4path = os.path.join(HDIR, 'yamls/file4.yaml')
        self.file5path = os.path.join(HDIR, 'yamls/file5.yaml')
        self.file6path = os.path.join(HDIR, 'yamls/file6.yaml')
        self.file7path = os.path.join(HDIR, 'yamls/file7.yaml')

    def test_load_raw_yaml(self):
        self.assertRaises(FileNotFoundError,
                          dw.load_yaml_file_to_dict, 'xxxx')
        self.assertRaises(dw.YamlParsingError,
                          dw.load_yaml_file_to_dict, self.file2path)
        result = dw.load_yaml_file_to_dict(self.file1path)
        self.assertTrue(isinstance(result, dict))

    def test_apply_yamldict_to_checksuite_keyerrors(self):
        checksuite = dw.PandasDatsetCheckSuite(self.df_file1)
        ymld = dw.load_yaml_file_to_dict(self.file3path)
        self.assertTrue(isinstance(ymld, dict))
        self.assertRaises(dw.YamlParsingError,
                          dw.apply_yamldict_to_checksuite,
                          ymld,
                          checksuite)
        ymld = dw.load_yaml_file_to_dict(self.file4path)
        self.assertRaises(dw.YamlParsingError,
                          dw.apply_yamldict_to_checksuite,
                          ymld,
                          checksuite)
        ymld = dw.load_yaml_file_to_dict(self.file5path)
        self.assertRaises(dw.YamlParsingError,
                          dw.apply_yamldict_to_checksuite,
                          ymld,
                          checksuite)
        ymld = dw.load_yaml_file_to_dict(self.file6path)
        self.assertRaises(dw.YamlParsingError,
                          dw.apply_yamldict_to_checksuite,
                          ymld,
                          checksuite)
        ymld = dw.load_yaml_file_to_dict(self.file7path)
        self.assertRaises(dw.YamlParsingError,
                          dw.apply_yamldict_to_checksuite,
                          ymld,
                          checksuite)
        # The following should not raise an error - test will
        # fail if it does
        ymld = dw.load_yaml_file_to_dict(self.file1path)
        dw.apply_yamldict_to_checksuite(ymld, checksuite)

    def test_apply_yamldict_to_checksuite_valuechecks(self):
        checksuite = dw.PandasDatsetCheckSuite(self.df_file1)
        ymld = dw.load_yaml_file_to_dict(self.file1path)
        dw.apply_yamldict_to_checksuite(ymld, checksuite)
        # Dataset checks
        self.assertFalse(checksuite.allow_duplicate_rows)
        self.assertTrue(checksuite.stop_on_fail)
        self.assertEqual(checksuite.row_count_max, 10)
        self.assertEqual(checksuite.row_count_min, 3)
        self.assertEqual(checksuite.row_count, 5)
        # Column checks
        self.assertEqual(len(checksuite.columns), 4)
        col1 = checksuite.columns[0]
        col2 = checksuite.columns[1]
        col3 = checksuite.columns[2]
        col9 = checksuite.columns[3]
        # col 1
        self.assertEqual(col1.name, 'A')
        self.assertEqual(col1.type, 'numeric')
        self.assertEqual(col1.allow_duplicates, False)
        self.assertEqual(col1.allow_nulls, True)
        self.assertEqual(col1.min_val, 0)
        self.assertEqual(col1.max_val, 5)
        self.assertEqual(col1.count_distinct_max, 10)
        self.assertEqual(col1.count_distinct_min, 1)
        self.assertEqual(col1.count_distinct, 5)
        # col 2
        self.assertEqual(col2.name, 'C')
        self.assertEqual(col2.type, 'string')
        self.assertEqual(col2.allow_blanks, False)
        self.assertEqual(col2.allow_nulls, False)
        self.assertEqual(col2.count_distinct_max, 10)
        self.assertEqual(col2.count_distinct_min, 1)
        self.assertEqual(col2.count_distinct, 5)
        self.assertEqual(col2.regex_type, 'mandatory')
        self.assertEqual(col2.regex_rule, '[a-m]')
        # col 3
        self.assertEqual(col3.name, 'I')
        self.assertEqual(col3.type, 'numeric')
        self.assertEqual(col3.allow_duplicates, True)
        self.assertEqual(col3.allow_nulls, True)
        self.assertEqual(col3.val, 1)
        # col 9
        self.assertEqual(col9.name, 'J')
        self.assertEqual(col9.type, 'datetime')
        self.assertEqual(col9.allow_nulls, False)
        self.assertEqual(col9.dateformat, '%m/%d/%Y')



if __name__ == '__main__':
    unittest.main()
