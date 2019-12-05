import inspect
import os
import unittest
HDIR = os.path.dirname(os.path.abspath(
            inspect.getfile(inspect.currentframe())))

loader = unittest.TestLoader()
suite = loader.discover(HDIR)
runner = unittest.TextTestRunner()
runner.run(suite)
