from typing import List, Tuple
import pandas as pd

import pandas_checks as pc


class DataSetCheckSuite:

    def __init__(self):
        self.fail: bool = False
        self.min_rows: int = 0
        self.allow_duplicate_rows: bool = True
        self.error_messages: [str] = []
        self._checks = []
        self.columns = []
        self.num_checks_done = 0

    def _assemble_checks(self):
        self._checks = []
        if self.min_rows > 0:
            self._checks.append(self.check_min_rows)
        if not self.allow_duplicate_rows:
            self._checks.append(self.check_allow_duplicate_rows)

    def run_checks(self):
        self.error_messages = []
        self.num_checks_done = 0
        self._assemble_checks()
        checks_failed: bool = False
        for check in self._checks:
            passed, message = check()
            self.num_checks_done += 1
            if not passed:
                self.error_messages.append(message)
                if self.fail:
                    checks_failed = True
                    break

    def check_min_rows(self) -> Tuple[bool, str]: raise NotImplementedError
    def check_allow_duplicate_rows(self) -> Tuple[bool, str]: raise NotImplementedError


class PandasDatsetCheckSuite(DataSetCheckSuite):

    def __init__(self, dataframe: pd.DataFrame):
        self.dataframe: pd.DataFrame = dataframe
        super().__init__()

    def check_min_rows(self) -> Tuple[bool, str]:
        return pc.dfcheck_min_rows(self.dataframe, self.min_rows)

    def check_allow_duplicate_rows(self) -> Tuple[bool, str]:
        return pc.dfcheck_no_duplicate_rows(self.dataframe)


class ColumnCheckSuite:

    def __init__(self, colname: str, coltype: str):
        self.name: str = colname
        self.type: str = coltype
        self._checks = []

    def _assemble_checks(self):
        self._checks = []
        self._checks.append(self.check_col_exists)
        self._checks.append(self.check_col_type)

    def check_col_exists(self) -> Tuple[bool, str]: raise NotImplementedError
    def check_col_type(self) -> Tuple[bool, str]: raise NotImplementedError


class PandasColumnCheckSuite(ColumnCheckSuite):

    def __init__(self, dataframe: pd.DataFrame):
        self.dataframe: pd.DataFrame = dataframe
        super().__init__()

    def check_col_exists(self) -> Tuple[bool, str]:
        return pc.colcheck_col_exists(self.dataframe, self.name)

    def check_col_type(self) -> Tuple[bool, str]:
        if self.type in ['int', 'float', 'numeric']:
            return pc.colcheck_is_numeric(self.dataframe, self.name)
        return False, 'Incomplete method'

