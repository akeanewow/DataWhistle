import inspect
import os
import sys
HDIR = os.path.dirname(os.path.abspath(
            inspect.getfile(inspect.currentframe())))
PARENTDIR = os.path.dirname(HDIR)
sys.path.insert(0, PARENTDIR)
import datawhistle as dw


def main():
    dw.commandline_main()


if __name__ == '__main__':
    main()
