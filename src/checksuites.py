import pandas as pd  # type: ignore
from typing import Callable, List, Tuple

import pandas_checks as pc


class DataSetCheckSuite:
    '''
    The DataSetCheckSuite object is used to run checks. Checks are implemented
    in child classes by overriding check_* methods to enable checking of
    different data sources.
    '''

    def __init__(self):
        # test settings
        self.fail: bool = False
        self.min_rows: int = 0
        self.allow_duplicate_rows: bool = True
        # other properties
        self.error_messages: [str] = []
        self.columns: List[PandasColumnCheckSuite] = []
        self._checks: List[Callable] = []

    def _assemble_checks(self) -> None:
        self._checks = []
        if self.min_rows > 0:
            self._checks.append(self.check_min_rows)
        if not self.allow_duplicate_rows:
            self._checks.append(self.check_allow_duplicate_rows)

    def run_checks(self) -> None:
        '''
        Run all checks based on object properties capturing test settings.
        '''
        self.error_messages = []
        self._assemble_checks()
        checks_failed: bool = False
        for check in self._checks:
            passed, message = check()
            if not passed:
                self.error_messages.append(message)
                if self.fail:
                    checks_failed = True
                    break
        if not checks_failed:
            for column in self.columns:
                error_messages = column.run_checks(self.fail)
                self.error_messages += error_messages
                if len(error_messages) > 0 & self.fail:
                    break

    def check_min_rows(self) -> Tuple[bool, str]:
        raise NotImplementedError

    def check_allow_duplicate_rows(self) -> Tuple[bool, str]:
        raise NotImplementedError


class ColumnCheckSuite:
    '''
    The ColumnCheckSuite object is used to run checks. Checks are implemented
    in child classes by overriding check_* methods to enable checking of
    different data sources.
    '''

    def __init__(self, colname: str, coltype: str):
        self.name: str = colname
        self.error_messages: List[str] = []
        self.type: str = coltype
        self._checks: List[Callable] = []

    def _assemble_checks(self) -> None:
        self._checks = []
        self._checks.append(self.check_col_type)

    def run_checks(self, fail: bool) -> List[str]:
        '''
        Run all checks based on object properties capturing test settings.
        '''
        passed, message = self.check_col_exists()
        if not passed:
            self.error_messages.append(message)
            return [message]
        self.error_messages = []
        self._assemble_checks()
        for check in self._checks:
            passed, message = check()
            if not passed:
                self.error_messages.append(message)
                if fail:
                    break
        return self.error_messages

    def check_col_exists(self) -> Tuple[bool, str]:
        raise NotImplementedError

    def check_col_type(self) -> Tuple[bool, str]:
        raise NotImplementedError


class PandasDatsetCheckSuite(DataSetCheckSuite):
    '''
    Pandas DataFrame testing object. Check methods from the parent class are
    overriden to implement Pandas specific functionality.
    '''

    def __init__(self, dataframe: pd.DataFrame):
        self.dataframe: pd.DataFrame = dataframe
        super().__init__()

    def check_min_rows(self) -> Tuple[bool, str]:
        return pc.dfcheck_min_rows(self.dataframe, self.min_rows)

    def check_allow_duplicate_rows(self) -> Tuple[bool, str]:
        return pc.dfcheck_no_duplicate_rows(self.dataframe)


class PandasColumnCheckSuite(ColumnCheckSuite):
    '''
    Pandas DataFrame column testing object. Check methods from the parent class
    are overriden to implement Pandas specific functionality.
    '''

    def __init__(self, dataframe: pd.DataFrame, colname: str, coltype: str):
        self.dataframe: pd.DataFrame = dataframe
        super().__init__(colname, coltype)

    def check_col_exists(self) -> Tuple[bool, str]:
        return pc.colcheck_col_exists(self.dataframe, self.name)

    def check_col_type(self) -> Tuple[bool, str]:
        if self.type == 'numeric':
            return pc.colcheck_is_numeric(self.dataframe, self.name)
        if self.type == 'string':
            return pc.colcheck_is_str(self.dataframe, self.name)
        return False, (f'column {self.name} could not tested '
                       f'for type {self.type} (unknown type)')
