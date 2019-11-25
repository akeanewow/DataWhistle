import unittest
import pandas as pd  # type: ignore
import sys
sys.path.append('../src')
import yaml_parsing as yp  # type: ignore
import checksuites as cs  # type: ignore


class TestYamlParsing(unittest.TestCase):

    def setUp(self):
        self.df_file1 = pd.read_csv('data/file1.csv')

    def test_load_raw_yaml(self):
        self.assertRaises(FileNotFoundError,
                          yp.load_yaml_file_to_dict, 'xxxx')
        self.assertRaises(yp.YamlParsingError,
                          yp.load_yaml_file_to_dict, 'yamls/file2.yaml')
        result = yp.load_yaml_file_to_dict('yamls/file1.yaml')
        self.assertTrue(isinstance(result, dict))

    def test_apply_yamldict_to_checksuite_keyerrors(self):
        checksuite = cs.PandasDatsetCheckSuite(self.df_file1)
        ymld = yp.load_yaml_file_to_dict('yamls/file3.yaml')
        self.assertTrue(isinstance(ymld, dict))
        self.assertRaises(yp.YamlParsingError,
                          yp.apply_yamldict_to_checksuite,
                          ymld,
                          checksuite)
        ymld = yp.load_yaml_file_to_dict('yamls/file4.yaml')
        self.assertRaises(yp.YamlParsingError,
                          yp.apply_yamldict_to_checksuite,
                          ymld,
                          checksuite)
        ymld = yp.load_yaml_file_to_dict('yamls/file5.yaml')
        self.assertRaises(yp.YamlParsingError,
                          yp.apply_yamldict_to_checksuite,
                          ymld,
                          checksuite)
        # The following should not raise an error - test will
        # fail if it does
        ymld = yp.load_yaml_file_to_dict('yamls/file1.yaml')
        yp.apply_yamldict_to_checksuite(ymld, checksuite)

    def test_apply_yamldict_to_checksuite_valuechecks(self):
        checksuite = cs.PandasDatsetCheckSuite(self.df_file1)
        ymld = yp.load_yaml_file_to_dict('yamls/file1.yaml')
        yp.apply_yamldict_to_checksuite(ymld, checksuite)
        # Dataset checks
        self.assertFalse(checksuite.allow_duplicate_rows)
        self.assertTrue(checksuite.stop_on_fail)
        self.assertEqual(checksuite.min_rows, 3)
        # Column checks
        self.assertEqual(len(checksuite.columns), 2)
        col1 = checksuite.columns[0]
        col2 = checksuite.columns[1]
        # col 1
        self.assertEqual(col1.name, 'A')
        self.assertEqual(col1.type, 'numeric')
        self.assertEqual(col1.allow_nulls, True)
        self.assertEqual(col1.min_val, 0)
        self.assertEqual(col1.count_distinct_max, 10)
        self.assertEqual(col1.count_distinct_min, 1)
        self.assertEqual(col1.count_distinct, 5)
        # col 2
        self.assertEqual(col2.name, 'C')
        self.assertEqual(col2.type, 'string')
        self.assertEqual(col2.allow_nulls, False)
        self.assertEqual(col1.count_distinct_max, 10)
        self.assertEqual(col1.count_distinct_min, 1)
        self.assertEqual(col1.count_distinct, 5)


if __name__ == '__main__':
    unittest.main()
