import argparse
import sys
import pandas as pd  # type: ignore
import datawhistle as dw


_HELP = ('A Programmatic Data Checker '
         '(see https://github.com/akeanewow/DataWhistle)')


def commandline_main() -> None:
    parser = argparse.ArgumentParser(description=_HELP)
    parser.add_argument("-c", "--csv", type=str,
                        help='a comma separated value file to check')
    parser.add_argument("-r", "--rules", type=str,
                        help='rules to apply defined in a yaml file')
    parser.add_argument("-v", "--verbose", action='store_true',
                        help='increase output verbosity')
    args = parser.parse_args()
    if args.csv and args.rules:
        commandline_check_csv(args.csv, args.rules, args.verbose)
        return
    print(('Data source e.g. CSV file and rules file required '
           '(use -h command line argument to get help)'))


def commandline_check_csv(csvfile: str, rulesfile: str, verbose: bool) -> None:
    '''Run checks on a CSV file.'''
    df = commandline_load_file_pandas(csvfile, verbose)
    if verbose:
        print('Parsing rules file ... ', end='')
    try:
        ymld = dw.load_yaml_file_to_dict(rulesfile)
        checksuite = dw.PandasDatsetCheckSuite(df)
        dw.apply_yamldict_to_checksuite(ymld, checksuite)
    except FileNotFoundError:
        print(f'File {rulesfile} not found')
        sys.exit(4)
    except dw.YamlParsingError as e:
        print(e)
        sys.exit(5)
    except Exception as ex:
        print(f'Unexpected YAML parsing error:\n{ex}')
        sys.exit(6)
    if verbose:
        print('done.\nRunning checks ', end='')
    checksuite.runchecks(verbose=verbose)
    num_errs = len(checksuite.error_messages)
    if num_errs > 0:
        if verbose:
            print(f' done.\nChecks failed ({num_errs}):')
        for msg in checksuite.error_messages:
            print(msg)
        sys.exit(1)
    else:
        if verbose:
            print(' done.\nAll checks passed.')


def commandline_load_file_pandas(csvfile: str, verbose: bool) -> pd.DataFrame:
    '''Load a data file into a Pandas DataFrame.'''
    if verbose:
        print('Reading data file ... ', end='')
    try:
        df = pd.read_csv(csvfile)
    except FileNotFoundError:
        print(f'File {csvfile} not found')
        sys.exit(2)
    except Exception as ex:
        print(f'Unexpected Pandas error:\n{ex}')
        sys.exit(3)
    if verbose:
        print('done.')
    return df
