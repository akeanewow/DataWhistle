import argparse
import sys
import pandas as pd  # type: ignore

import checksuites as cs
import yaml_parsing as yp


_HELP = ('A Programmatic Data Checker '
         '(see https://github.com/akeanewow/DataWhistle)')


def main() -> None:
    parser = argparse.ArgumentParser(description=_HELP)
    parser.add_argument("-c", "--csv", type=str,
                        help='a comma separated value file to check')
    parser.add_argument("-r", "--rules", type=str,
                        help='rules to apply defined in a yaml file')
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
    df = load_file_pandas(filename, verbose)
    if verbose:
        print('Parsing rules file ... ', end='')
    ymld = yp.load_yaml_file_to_dict(rulesfilename)
    checksuite = cs.PandasDatsetCheckSuite(df)
    yp.apply_yamldict_to_checksuite(ymld, checksuite)
    if verbose:
        print('done.\nRunning checks ', end='')
    checksuite.run_checks(verbose=verbose)
    if len(checksuite.error_messages) > 0:
        if verbose:
            print(' done.\nChecks failed:')
        for msg in checksuite.error_messages:
            print(msg)
        sys.exit(1)
    else:
        if verbose:
            print(' done.\nAll checks passed.')


def load_file_pandas(filename: str, verbose: bool) -> pd.DataFrame:
    if verbose:
        print('Reading data file ... ', end='')
    try:
        df = pd.read_csv(filename)
    except FileNotFoundError:
        print(f'\nFile {filename} not found')
        sys.exit(2)
    except Exception as ex:
        print(f'\nUnexpected error:\n{ex}')
        sys.exit(3)
    if verbose:
        print('done.')
    return df


if __name__ == '__main__':
    main()
