import unittest
import io
import sys
sys.path.append('..')
import datawhistle as dw


_ALL_PASSED = '''Reading data file ... done.
Parsing rules file ... done.
Running checks .................... done.
All checks passed.
'''

_ALL_FAILED = '''Reading data file ... done.
Parsing rules file ... done.
Running checks FFFF.FFFFFF..FFF....FFFF..FF done.
Checks failed (19):
want 0 duplicate rows, got 2
want row count <= 1, got 7
want row count >= 8, got 7
want row count == 6, got 7
column A expected to be string type but is not
column A cannot check minimum value on a non-numeric column
column A cannot check maximum value on a non-numeric column
column A want count distinct <= 1, got 5
column A want count distinct >= 10, got 5
column A want count distinct == 7, got 5
column B want value >= 10.1, got 1.0
column B want value <= 3.0, got 5.4
column B want all values = 1.0, got different values
column D want 0 nulls, got 2
column D want count distinct <= 1, got 3
column D want count distinct >= 10, got 3
column D want count distinct == 4, got 3
column F want 0 nulls, got 2
column X not found in data
'''


class TestWhistle(unittest.TestCase):

    def setUp(self):
        self.maxDiff = None
        self.capturedStout = io.StringIO()
        sys.stdout = self.capturedStout

    def tearDown(self):
        sys.stdout = sys.__stdout__

    def test_allpassed_silent(self):
        dw.commandline_check_csv('data/file1.csv', 'yamls/file1.yaml',
                                 False)
        self.assertEqual(self.capturedStout.getvalue(), '')

    def test_allpassed_verbose(self):
        dw.commandline_check_csv('data/file1.csv', 'yamls/file1.yaml',
                                 True)
        self.assertEqual(self.capturedStout.getvalue(), _ALL_PASSED)

    def test_csvfile_not_found(self):
        with self.assertRaises(SystemExit) as e:
            dw.commandline_check_csv('data/zile1.csv',
                                     'yamls/file1.yaml', True)
        self.assertEqual(e.exception.code, 2)

    def test_yamlfile_not_found(self):
        with self.assertRaises(SystemExit) as e:
            dw.commandline_check_csv('data/file1.csv',
                                     'yamls/zile1.yaml', True)
        self.assertEqual(e.exception.code, 4)

    def test_yamlerror(self):
        with self.assertRaises(SystemExit) as e:
            dw.commandline_check_csv('data/file1.csv',
                                     'yamls/file3.yaml', True)
        self.assertEqual(e.exception.code, 5)

    def test_all_failed(self):
        with self.assertRaises(SystemExit) as e:
            dw.commandline_check_csv('data/file2.csv', 'yamls/file1a.yaml',
                                     True)
        self.assertEqual(e.exception.code, 1)
        self.assertEqual(self.capturedStout.getvalue(), _ALL_FAILED)


if __name__ == '__main__':
    unittest.main()
