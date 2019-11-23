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
Running checks ...
All checks passed.
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


if __name__ == '__main__':
    unittest.main()
