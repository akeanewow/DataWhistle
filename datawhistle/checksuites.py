# Avoid forward decalaration type check errors. See PEP563.
from __future__ import annotations
from typing import Callable, Optional, List, Tuple, Union
import pandas as pd  # type: ignore
import datawhistle.pandaschecks as dwpc
import datawhistle.bqchecks as dwbc


class TableCheckSuite:
    '''
    The TableCheckSuite object is used to run checks. Checks are implemented
    in child classes by overriding check_* methods to enable checking of
    different data sources.
    '''

    def __init__(self):
        # test settings
        self.allow_duplicate_rows: bool = True
        self.row_count_max: Optional[int] = None
        self.row_count_min: Optional[int] = None
        self.row_count: Optional[int] = None
        self.stop_on_fail: bool = False
        # other properties
        self.error_messages: [str] = []
        self.columns: List[Union[PandasColumnCheckSuite,
                                 BqColumnCheckSuite]] = []
        self._checks: List[Callable] = []

    def _assemble_checks(self) -> None:
        self._checks = []
        if not self.allow_duplicate_rows:
            self._checks.append(self.check_no_duplicate_rows)
        if self.row_count_max is not None:
            self._checks.append(self.check_row_count_max)
        if self.row_count_min is not None:
            self._checks.append(self.check_row_count_min)
        if self.row_count is not None:
            self._checks.append(self.check_row_count)

    def runchecks(self, verbose: bool = False) -> None:
        '''
        Run all checks based on object properties capturing test settings.
        '''
        self.error_messages = []
        self._assemble_checks()
        checks_failed: bool = False
        for check in self._checks:
            passed, message = check()
            if not passed:
                if verbose:
                    print('F', end='', flush=True)
                self.error_messages.append(message)
                if self.stop_on_fail:
                    checks_failed = True
                    break
            else:
                if verbose:
                    print('.', end='', flush=True)
        if not checks_failed:
            for column in self.columns:
                error_messages = column.runchecks(self.stop_on_fail,
                                                  verbose=verbose)
                self.error_messages += error_messages
                if len(error_messages) > 0 and self.stop_on_fail:
                    break

    def clearcolumns(self) -> None:
        '''Clear column rules to add new rules.'''
        self.columns = []

    def addcolumn(self, colname: str,
                  coltype: str) -> Union[PandasColumnCheckSuite,
                                         BqColumnCheckSuite]:
        raise NotImplementedError

    def check_row_count_max(self) -> Tuple[bool, str]:
        raise NotImplementedError

    def check_row_count_min(self) -> Tuple[bool, str]:
        raise NotImplementedError

    def check_row_count(self) -> Tuple[bool, str]:
        raise NotImplementedError

    def check_no_duplicate_rows(self) -> Tuple[bool, str]:
        raise NotImplementedError


class ColumnCheckSuite:
    '''
    The ColumnCheckSuite object is used to run checks. Checks are implemented
    in child classes by overriding check_* methods to enable checking of
    different data sources.
    '''

    def __init__(self, colname: str, coltype: str):
        # test settings
        self.columnname: str = colname
        self.type: str = coltype
        self.allow_blanks: bool = True
        self.allow_duplicates: bool = True
        self.allow_nulls: bool = True
        self.allow_outliers: bool = True
        self.count_distinct_max: Optional[int] = None
        self.count_distinct_min: Optional[int] = None
        self.count_distinct: Optional[int] = None
        self.min_val: Optional[Union[int, float]] = None
        self.max_val: Optional[Union[int, float]] = None
        self.val: Optional[Union[int, float]] = None
        self.dateformat: Optional[str] = None
        self.regex_rule: Optional[str] = None
        self.regex_type: Optional[str] = None
        # other properties
        self.error_messages: List[str] = []
        self._checks: List[Callable] = []

    def _assemble_checks(self) -> None:
        self._checks = []
        self._checks.append(self.check_col_type)
        if not self.allow_blanks:
            self._checks.append(self.check_col_no_blanks)
        if not self.allow_duplicates:
            self._checks.append(self.check_col_no_duplicates)
        if not self.allow_nulls:
            self._checks.append(self.check_col_non_nulls)
        if not self.allow_outliers:
            self._checks.append(self.check_col_iqr)
        if self.count_distinct_max is not None:
            self._checks.append(self.check_col_count_distinct_max)
        if self.count_distinct_min is not None:
            self._checks.append(self.check_col_count_distinct_min)
        if self.count_distinct is not None:
            self._checks.append(self.check_col_count_distinct)
        if self.min_val is not None:
            self._checks.append(self.check_col_min_val)
        if self.max_val is not None:
            self._checks.append(self.check_col_max_val)
        if self.val is not None:
            self._checks.append(self.check_col_val)
        if self.regex_rule is not None:
            self._checks.append(self.check_col_regex)

    def runchecks(self, stop_on_fail: bool,
                  verbose: bool = False) -> List[str]:
        '''
        Run all checks based on object properties capturing test settings.
        '''
        # have to always check if a column exists otherwise all
        # other column checks will fail anyway
        passed, message = self.check_col_exists()
        if not passed:
            if verbose:
                print('F', end='')
            self.error_messages.append(message)
            return [message]
        else:
            if verbose:
                print('.', end='')
        # keep going with tests if the column exists
        self.error_messages = []
        self._assemble_checks()
        for check in self._checks:
            passed, message = check()
            if not passed:
                if verbose:
                    print('F', end='', flush=True)
                self.error_messages.append(message)
                if stop_on_fail:
                    break
            else:
                if verbose:
                    print('.', end='', flush=True)
        return self.error_messages

    def check_col_count_distinct_max(self) -> Tuple[bool, str]:
        raise NotImplementedError

    def check_col_count_distinct_min(self) -> Tuple[bool, str]:
        raise NotImplementedError

    def check_col_count_distinct(self) -> Tuple[bool, str]:
        raise NotImplementedError

    def check_col_exists(self) -> Tuple[bool, str]:
        raise NotImplementedError

    def check_col_min_val(self) -> Tuple[bool, str]:
        raise NotImplementedError

    def check_col_max_val(self) -> Tuple[bool, str]:
        raise NotImplementedError

    def check_col_no_blanks(self) -> Tuple[bool, str]:
        raise NotImplementedError

    def check_col_no_duplicates(self) -> Tuple[bool, str]:
        raise NotImplementedError

    def check_col_non_nulls(self) -> Tuple[bool, str]:
        raise NotImplementedError

    def check_col_regex(self) -> Tuple[bool, str]:
        raise NotImplementedError

    def check_col_iqr(self) -> Tuple[bool, str]:
        raise NotImplementedError

    def check_col_val(self) -> Tuple[bool, str]:
        raise NotImplementedError

    def check_col_type(self) -> Tuple[bool, str]:
        raise NotImplementedError


class PandasDatsetCheckSuite(TableCheckSuite):
    '''
    Pandas DataFrame testing object. Check methods from the parent class are
    overriden to implement Pandas specific functionality.
    '''

    def __init__(self, dataframe: pd.DataFrame):
        self.dataframe: pd.DataFrame = dataframe
        super().__init__()

    def addcolumn(self, colname: str, coltype: str) -> PandasColumnCheckSuite:
        '''Add a column to set rules on.'''
        column = PandasColumnCheckSuite(self.dataframe, colname, coltype)
        self.columns.append(column)
        return column

    def check_row_count_max(self) -> Tuple[bool, str]:
        if self.row_count_max is None:
            return True, ''
        val = int(self.row_count_max)
        return dwpc.dfcheck_row_count(self.dataframe, val, '<=')

    def check_row_count_min(self) -> Tuple[bool, str]:
        if self.row_count_min is None:
            return True, ''
        val = int(self.row_count_min)
        return dwpc.dfcheck_row_count(self.dataframe, val, '>=')

    def check_row_count(self) -> Tuple[bool, str]:
        if self.row_count is None:
            return True, ''
        val = int(self.row_count)
        return dwpc.dfcheck_row_count(self.dataframe, val, '==')

    def check_no_duplicate_rows(self) -> Tuple[bool, str]:
        return dwpc.dfcheck_no_duplicate_rows(self.dataframe)


class PandasColumnCheckSuite(ColumnCheckSuite):
    '''
    Pandas DataFrame column testing object. Check methods from the parent class
    are overriden to implement Pandas specific functionality.
    '''

    def __init__(self, dataframe: pd.DataFrame, colname: str, coltype: str):
        self.dataframe: pd.DataFrame = dataframe
        super().__init__(colname, coltype)

    def check_col_count_distinct_max(self) -> Tuple[bool, str]:
        if self.count_distinct_max is None:
            return True, ''
        max_val = int(self.count_distinct_max)
        return dwpc.colcheck_count_distinct(self.dataframe, self.columnname,
                                            max_val, '<=')

    def check_col_count_distinct_min(self) -> Tuple[bool, str]:
        if self.count_distinct_min is None:
            return True, ''
        min_val = int(self.count_distinct_min)
        return dwpc.colcheck_count_distinct(self.dataframe, self.columnname,
                                            min_val, '>=')

    def check_col_count_distinct(self) -> Tuple[bool, str]:
        if self.count_distinct is None:
            return True, ''
        val = int(self.count_distinct)
        return dwpc.colcheck_count_distinct(self.dataframe, self.columnname,
                                            val, '==')

    def check_col_exists(self) -> Tuple[bool, str]:
        return dwpc.colcheck_exists(self.dataframe, self.columnname)

    def check_col_min_val(self) -> Tuple[bool, str]:
        if not self.type == 'numeric':
            return False, (f'column {self.columnname} cannot check minimum '
                           'value on a non-numeric column')
        if self.min_val is None:
            return False, (f'column {self.columnname} could not check '
                           'minimum value')
        min_val = float(self.min_val)
        return dwpc.colcheck_val(self.dataframe, self.columnname, min_val,
                                 '>=')

    def check_col_max_val(self) -> Tuple[bool, str]:
        if not self.type == 'numeric':
            return False, (f'column {self.columnname} cannot check maximum '
                           'value on a non-numeric column')
        if self.max_val is None:
            return False, (f'column {self.columnname} could not check '
                           'maximum value')
        max_val = float(self.max_val)
        return dwpc.colcheck_val(self.dataframe, self.columnname, max_val,
                                 '<=')

    def check_col_iqr(self) -> Tuple[bool, str]:
        if not self.type == 'numeric':
            return False, (f'column (self.columnname) cannot check '
                           'inter-quartile range on a non-numeric column')
        return dwpc.colcheck_iqr(self.dataframe, self.columnname)

    def check_col_no_blanks(self) -> Tuple[bool, str]:
        if not self.type == 'string':
            return False, (f'column {self.columnname} cannot check for blanks '
                           'in non-string column')
        return dwpc.colcheck_no_blanks(self.dataframe, self.columnname)

    def check_col_no_duplicates(self) -> Tuple[bool, str]:
        return dwpc.colcheck_no_duplicates(self.dataframe, self.columnname)

    def check_col_non_nulls(self) -> Tuple[bool, str]:
        return dwpc.colcheck_no_nulls(self.dataframe, self.columnname)

    def check_col_val(self) -> Tuple[bool, str]:
        if not self.type == 'numeric':
            return False, (f'column {self.columnname} cannot check '
                           'value of a non-numeric column')
        if self.val is None:
            return False, (f'column {self.columnname} could not check value')
        val = float(self.val)
        return dwpc.colcheck_val(self.dataframe, self.columnname, val, '==')

    def check_col_type(self) -> Tuple[bool, str]:
        if self.type == 'numeric':
            return dwpc.colcheck_is_numeric(self.dataframe, self.columnname)
        if self.type == 'string':
            return dwpc.colcheck_is_str(self.dataframe, self.columnname)
        if self.type == 'datetime':
            success, msg = dwpc.colcheck_is_datetime(self.dataframe,
                                                     self.columnname,
                                                     self.dateformat)
            if success:
                if self.dateformat is not None:
                    pd.to_datetime(self.dataframe[self.columnname],
                                   format=self.dateformat)
                else:
                    pd.to_datetime(self.dataframe[self.columnname])
            return success, msg
        return False, (f'column {self.columnname} could not tested '
                       f'for type {self.type} (unknown type)')

    def check_col_regex(self) -> Tuple[bool, str]:
        return dwpc.colcheck_regex(self.dataframe, self.columnname,
                                   self.regex_rule, self.regex_type)


class BqTableCheckSuite(TableCheckSuite):
    '''
    BigQuery table testing object. Check methods from the parent class are
    overriden to implement BigQuery specific functionality.
    '''

    def __init__(self, datasetname: str, tablename: str):
        super().__init__()
        self.datasetname = datasetname
        self.tablename = tablename

    # Implement an extension on the parent runchecks method to add a check
    # if the table exists before proceeding.
    def runchecks(self, verbose: bool = False) -> None:
        '''
        Run all checks based on object properties capturing test settings.
        '''
        passed, message = dwbc.dscheck_table_exists(self.datasetname,
                                                    self.tablename)
        if not passed:
            self.error_messages = []
            self.error_messages.append(message)
            return
        super().runchecks(verbose)

    def addcolumn(self, columnname: str,
                  columntype: str) -> BqColumnCheckSuite:
        '''Add a column to set rules on.'''
        column = BqColumnCheckSuite(self.datasetname, self.tablename,
                                    columnname, columntype)
        self.columns.append(column)
        return column

    def check_row_count_max(self) -> Tuple[bool, str]:
        if self.row_count_max is None:
            return True, ''
        val = int(self.row_count_max)
        return dwbc.dscheck_row_count(self.datasetname, self.tablename,
                                      val, '<=')

    def check_row_count_min(self) -> Tuple[bool, str]:
        if self.row_count_min is None:
            return True, ''
        val = int(self.row_count_min)
        return dwbc.dscheck_row_count(self.datasetname, self.tablename,
                                      val, '>=')

    def check_row_count(self) -> Tuple[bool, str]:
        if self.row_count is None:
            return True, ''
        val = int(self.row_count)
        return dwbc.dscheck_row_count(self.datasetname, self.tablename,
                                      val, '==')

    def check_no_duplicate_rows(self) -> Tuple[bool, str]:
        return False, 'Cannot check BigQuery for duplicate rows'


class BqColumnCheckSuite(ColumnCheckSuite):
    '''
    BigQuery column testing object. Check methods from the parent class
    are overriden to implement BigQuery specific functionality.
    '''

    def __init__(self, datasetname: str, tablename: str, columnname: str,
                 columntype: str):
        super().__init__(columnname, columntype)
        self.datasetname = datasetname
        self.tablename = tablename

    def check_col_count_distinct_max(self) -> Tuple[bool, str]:
        if self.count_distinct_max is None:
            return True, ''
        max_val = int(self.count_distinct_max)
        return dwbc.colcheck_count_distinct(self.datasetname, self.tablename,
                                            self.columnname, max_val, '<=')

    def check_col_count_distinct_min(self) -> Tuple[bool, str]:
        if self.count_distinct_min is None:
            return True, ''
        min_val = int(self.count_distinct_min)
        return dwbc.colcheck_count_distinct(self.datasetname, self.tablename,
                                            self.columnname, min_val, '>=')

    def check_col_count_distinct(self) -> Tuple[bool, str]:
        if self.count_distinct is None:
            return True, ''
        val = int(self.count_distinct)
        return dwbc.colcheck_count_distinct(self.datasetname, self.tablename,
                                            self.columnname, val, '==')

    def check_col_exists(self) -> Tuple[bool, str]:
        return dwbc.colcheck_exists(self.datasetname, self.tablename,
                                    self.columnname)

    def check_col_min_val(self) -> Tuple[bool, str]:
        if not self.type == 'numeric':
            return False, (f'column {self.columnname} cannot check minimum '
                           'value on a non-numeric column')
        if self.min_val is None:
            return False, (f'column {self.columnname} could not check '
                           'minimum value')
        min_val = float(self.min_val)
        return dwbc.colcheck_val(self.datasetname, self.tablename,
                                 self.columnname, min_val, '>=')

    def check_col_max_val(self) -> Tuple[bool, str]:
        if not self.type == 'numeric':
            return False, (f'column {self.columnname} cannot check maximum '
                           'value on a non-numeric column')
        if self.max_val is None:
            return False, (f'column {self.columnname} could not check '
                           'maximum value')
        max_val = float(self.max_val)
        return dwbc.colcheck_val(self.datasetname, self.tablename,
                                 self.columnname, max_val, '<=')

    def check_col_iqr(self) -> Tuple[bool, str]:
        if not self.type == 'numeric':
            return False, (f'column (self.columnname) cannot check '
                           'inter-quartile range on a non-numeric column')
        return dwbc.colcheck_iqr(self.datasetname, self.tablename,
                                 self.columnname)

    def check_col_no_blanks(self) -> Tuple[bool, str]:
        if not self.type == 'string':
            return False, (f'column {self.columnname} cannot check for blanks '
                           'in non-string column')
        return dwbc.colcheck_no_blanks(self.datasetname, self.tablename,
                                       self.columnname)

    def check_col_no_duplicates(self) -> Tuple[bool, str]:
        return dwbc.colcheck_no_duplicates(self.datasetname, self.tablename,
                                           self.columnname)

    def check_col_non_nulls(self) -> Tuple[bool, str]:
        return dwbc.colcheck_no_nulls(self.datasetname, self.tablename,
                                      self.columnname)

    def check_col_regex(self) -> Tuple[bool, str]:
        return dwbc.colcheck_regex(self.datasetname, self.tablename,
                                   self.columnname, self.regex_rule,
                                   self.regex_type)

    def check_col_val(self) -> Tuple[bool, str]:
        if not self.type == 'numeric':
            return False, (f'column {self.columnname} cannot check '
                           'value of a non-numeric column')
        if self.val is None:
            return False, (f'column {self.columnname} could not check value')
        val = float(self.val)
        return dwbc.colcheck_val(self.datasetname, self.tablename,
                                 self.columnname, val, '==')

    def check_col_type(self) -> Tuple[bool, str]:
        if self.type == 'numeric':
            return dwbc.colcheck_is_numeric(self.datasetname, self.tablename,
                                            self.columnname)
        if self.type == 'string':
            return dwbc.colcheck_is_str(self.datasetname, self.tablename,
                                        self.columnname)
        if self.type == 'datetime':
            return dwbc.colcheck_is_datetime(self.datasetname, self.tablename,
                                             self.columnname)
        return False, (f'column {self.columnname} could not tested '
                       f'for type {self.type} (unknown type)')
