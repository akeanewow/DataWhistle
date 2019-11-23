import unittest
import subprocess


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
Running checks ....... done.
All checks passed.
'''

_ALL_FAILED = '''want 0 duplicate rows, got 2
want 10 rows, got 7
column A expected to be string type but is not
column A cannot check minimum value on a non-numeric column
column B want 10.1 minimum value, got 1.0
'''


class TestWhistle(unittest.TestCase):

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

    def test_allpassed_silent(self):
        result = subprocess.run(['python3', '../src/whistle.py',
                                 '-c', 'data/file1.csv',
                                 '-r', 'yamls/file1.yaml'],
                                capture_output=True, text=True)
        self.assertEqual(result.returncode, 0)
        self.assertEqual(result.stdout, '')

    def test_allpassed_verbose(self):
        result = subprocess.run(['python3', '../src/whistle.py',
                                 '-c', 'data/file1.csv',
                                 '-r', 'yamls/file1.yaml', '-v'],
                                capture_output=True, text=True)
        self.assertEqual(result.returncode, 0)
        self.assertEqual(result.stdout, _ALL_PASSED)

    def test_csvfile_not_found(self):
        result = subprocess.run(['python3', '../src/whistle.py',
                                 '-c', 'data/zile1.csv',
                                 '-r', 'yamls/file1.yaml'],
                                capture_output=True, text=True)
        self.assertEqual(result.returncode, 2)
        self.assertEqual(result.stdout, 'File data/zile1.csv not found\n')

    def test_yamlfile_not_found(self):
        result = subprocess.run(['python3', '../src/whistle.py',
                                 '-c', 'data/file1.csv',
                                 '-r', 'yamls/zile1.yaml'],
                                capture_output=True, text=True)
        self.assertEqual(result.returncode, 4)
        self.assertEqual(result.stdout, 'File yamls/zile1.yaml not found\n')

    def test_yamlerror(self):
        result = subprocess.run(['python3', '../src/whistle.py',
                                 '-c', 'data/file1.csv',
                                 '-r', 'yamls/file3.yaml'],
                                capture_output=True, text=True)
        self.assertEqual(result.returncode, 5)
        self.assertEqual(result.stdout, 'unexpected yaml attribute: stuff\n')

    def test_all_failed(self):
        result = subprocess.run(['python3', '../src/whistle.py',
                                 '-c', 'data/file2.csv',
                                 '-r', 'yamls/file1a.yaml'],
                                capture_output=True, text=True)
        self.assertEqual(result.returncode, 1)
        self.assertEqual(result.stdout, _ALL_FAILED)


if __name__ == '__main__':
    unittest.main()
