import unittest
import subprocess
import io
import sys
sys.path.append('../src')

import yaml_parsing as yp  # type: ignore
import whistle  # type: ignore


_HELP = '''usage: whistle.py [-h] [-c CSV] [-r RULES] [-v]

A Programmatic Data Checker (see https://github.com/akeanewow/DataWhistle)

optional arguments:
  -h, --help            show this help message and exit
  -c CSV, --csv CSV     a comma separated value file to check
  -r RULES, --rules RULES
                        rules to apply defined in a yaml file
  -v, --verbose         increase output verbosity
'''

_NOARGS = ('Data source e.g. CSV file and rules file required (use -h '
           'command line argument to get help)\n')

_ALL_PASSED = '''Reading data file ... done.
Parsing rules file ... done.
Running checks .............. done.
All checks passed.
'''

_ALL_FAILED = '''Reading data file ... done.
Parsing rules file ... done.
Running checks FF.FFFFF..F....FFFF..FF done.
Checks failed (14):
want 0 duplicate rows, got 2
want 10 rows, got 7
column A expected to be string type but is not
column A cannot check minimum value on a non-numeric column
column A want count distinct < 1, got 5
column A want count distinct > 10, got 5
column A want count distinct = 7, got 5
column B want 10.1 minimum value, got 1.0
column D want 0 nulls, got 2
column D want count distinct < 1, got 3
column D want count distinct > 10, got 3
column D want count distinct = 4, got 3
column F want 0 nulls, got 2
column X not found in data
'''


class TestCommandLine(unittest.TestCase):

    def test_help(self):
        result = subprocess.run(['python3', '../src/whistle.py', '-h'],
                                capture_output=True, text=True)
        self.assertEqual(result.returncode, 0)
        self.assertEqual(result.stdout, _HELP)

    def test_noargs(self):
        result = subprocess.run(['python3', '../src/whistle.py'],
                                capture_output=True, text=True)
        self.assertEqual(result.returncode, 0)
        self.assertEqual(result.stdout, _NOARGS)


class TestWhistle(unittest.TestCase):

    def setUp(self):
        self.capturedStout = io.StringIO()
        sys.stdout = self.capturedStout

    def tearDown(self):
        sys.stdout = sys.__stdout__

    def test_allpassed_silent(self):
        whistle.check_csv('data/file1.csv', 'yamls/file1.yaml',
                          False)
        self.assertEqual(self.capturedStout.getvalue(), '')

    def test_allpassed_verbose(self):
        whistle.check_csv('data/file1.csv', 'yamls/file1.yaml',
                          True)
        self.assertEqual(self.capturedStout.getvalue(), _ALL_PASSED)

    def test_csvfile_not_found(self):
        with self.assertRaises(SystemExit) as e:
            whistle.check_csv('data/zile1.csv', 'yamls/file1.yaml', True)
        self.assertEqual(e.exception.code, 2)

    def test_yamlfile_not_found(self):
        with self.assertRaises(SystemExit) as e:
            whistle.check_csv('data/file1.csv', 'yamls/zile1.yaml', True)
        self.assertEqual(e.exception.code, 4)

    def test_yamlerror(self):
        with self.assertRaises(SystemExit) as e:
            whistle.check_csv('data/file1.csv', 'yamls/file3.yaml', True)
        self.assertEqual(e.exception.code, 5)

    def test_all_failed(self):
        with self.assertRaises(SystemExit) as e:
            whistle.check_csv('data/file2.csv', 'yamls/file1a.yaml',
                              True)
        self.assertEqual(e.exception.code, 1)
        self.assertEqual(self.capturedStout.getvalue(), _ALL_FAILED)


if __name__ == '__main__':
    unittest.main()
