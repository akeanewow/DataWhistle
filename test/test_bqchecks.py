import inspect
import os
import sys
import unittest
HDIR = os.path.dirname(os.path.abspath(
            inspect.getfile(inspect.currentframe())))
PARENTDIR = os.path.dirname(HDIR)
sys.path.insert(0, PARENTDIR)
import datawhistle.bqchecks as dwbc


class TestDFChecks(unittest.TestCase):

    def setUp(self):
        pass


if __name__ == '__main__':
    unittest.main()
