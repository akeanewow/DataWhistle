import argparse
import sys
import pandas as pd  # type: ignore
import datawhistle as dw


_HELP = ('A Programmatic Data Checker '
         '(see https://github.com/akeanewow/DataWhistle)')


def commandline_main() -> None:
    parser = argparse.ArgumentParser(description=_HELP)
    parser.add_argument('-s', '--source', type=str, choices=['CSV', 'BQ'],
                        help='data source: CSV or BQ (BigQuery)')
    parser.add_argument('-f', '--file', type=str,
                        help='a comma separated value file to check')
    parser.add_argument('-r', '--rules', type=str,
                        help='rules to apply defined in a yaml file')
    parser.add_argument('-d', '--dataset', type=str,
                        help='dataset with table to check')
    parser.add_argument('-t', '--table', type=str,
                        help='table to check')
    parser.add_argument('-v', '--verbose', action='store_true',
                        help='increase output verbosity')
    args = parser.parse_args()
    if args.source and args.rules:
        if args.source == 'CSV' and args.file:
            commandline_check_csv(args.file, args.rules, args.verbose)
            return
        if args.dataset and args.table:
            commandline_check_bq(args.dataset, args.table, args.rules,
                                 args.verbose)
            return
    print(('Data source and rules file required '
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


def commandline_check_bq(datasetname: str, tablename: str, rulesfile: str,
                         verbose: bool) -> None:
    '''Run checks on a BigQuery table.'''
    if verbose:
        print('Parsing rules file ... ', end='')
    try:
        ymld = dw.load_yaml_file_to_dict(rulesfile)
        checksuite = dw.BqTableCheckSuite(datasetname, tablename)
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
