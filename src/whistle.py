import argparse
import sys
import pandas as pd  # type: ignore

import pandas_checks as pc
import checksuites as cs
import yaml_parsing as yp


_HELP = ('A Programmatic Data Checker '
         '(see https://github.com/akeanewow/DataWhistle)')


def main() -> None:
   parser = argparse.ArgumentParser(description=_HELP)
   parser.add_argument("-c", "--csv", type=str,
                       help='a comma separated value file to check')
   parser.add_argument("-r", "--rules", type=str,
                       help='rules to check defined in a yaml file')
   parser.add_argument("-v", "--verbose", action='store_true',
                       help='increase output verbosity')
   args = parser.parse_args()
   if args.csv and args.rules:
       check_csv(args.csv, args.rules, args.verbose)
       return
   print(('Data source e.g. CSV file and rules file required '
          '(use -h command line argument to get help)'))


def check_csv(filename: str, rulesfilename: str, verbose: bool) -> None:
    '''Run checks on a CSV file.'''
    if verbose:
        print('Reading csv file ... ', end='')
    df = pd.read_csv(filename)
    if verbose:
        print('done.\nParsing rules file ... ', end='')
    ymld = yp.load_yaml_file_to_dict(rulesfilename)
    checksuite = cs.PandasDatsetCheckSuite(df)
    yp.apply_yamldict_to_checksuite(ymld, checksuite)
    if verbose:
        print('done.\nRunning checks ...')
    checksuite.run_checks()
    if len(checksuite.error_messages) > 0:
        if verbose:
            print('Checks failed:')
        for msg in checksuite.error_messages:
            print(msg)
        sys.exit(1)
    else:
        if verbose:
            print('All checks passed.')


if __name__ == '__main__':
    main()
