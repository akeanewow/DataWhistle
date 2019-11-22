import unittest
import sys
sys.path.append('../src')
import yaml_parsing as yp  # type: ignore


class TestYamlParsing(unittest.TestCase):

    def test_load_raw_yaml(self):
        self.assertRaises(FileNotFoundError,
                          yp.load_yaml_file_to_dict, 'xxxx')
        self.assertRaises(yp.YamlParsingError,
                          yp.load_yaml_file_to_dict, 'yamls/file2.yaml')
        self.assertTrue(
                isinstance(yp.load_yaml_file_to_dict('yamls/file1.yaml'),
                           dict))


if __name__ == '__main__':
    unittest.main()
