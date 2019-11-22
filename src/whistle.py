import argparse

import pandas_checks as pc
import checksuites as cs
import yaml_parsing as yp


_HELP = ('A Programmatic Data Checker. '
         'See https://github.com/akeanewow/DataWhistle')


def main() -> None:
   parser = argparse.ArgumentParser(description=_HELP)
   parser.add_argument("--csv", help='a comma separated value file to check')
   parser.add_argument("--rules", help='rules to check defined in a yaml file')
   args = parser.parse_args()
   if args.csv and args.rules:
       print(f'csv={args.csv} rules={args.rules}')
   print('Both --csv and --rules arguments required (see --help)')


if __name__ == '__main__':
    main()
