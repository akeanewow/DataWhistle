from typing import Tuple
import pandas as pd  # type: ignore


# DataFrame level checks (as opposed to column level checks)
# are described in functions using the naming convention
# dfcheck_[some name](df: pd.DataFrame, [inputs]) -> Tuple[bool, str].
# The return value is a tuple containing a bool indicating if the
# test passed or failed (true = passed) and a string describing
# the error condition if the test failed. Error messages follow
# the pattern 'want [expected value or condition], got [actual
# value or condition]'.


def dfcheck_row_count(df: pd.DataFrame, count: int,
                      operator: str = '==') -> Tuple[bool, str]:
    '''
    Check if the number of rows in a dataset is equal to, greater
    than or less than a specified count.

    The operator parameter can be '==', '>=' or '<='.
    '''
    num_rows: int = len(df)
    if operator == '==' and num_rows == count:
        return True, ''
    if operator == '>=' and num_rows >= count:
        return True, ''
    if operator == '<=' and num_rows <= count:
        return True, ''
    if operator not in ['==', '<=', '>=']:
        return False, (f'dataset row count '
                       f'operator {operator} not recognised')
    return False, f'want row count {operator} {count}, got {num_rows}'


def dfcheck_no_duplicate_rows(df: pd.DataFrame) -> Tuple[bool, str]:
    '''Check if a DataFrame has duplicate rows.'''
    num_duplicates: int = sum(df.duplicated())
    if num_duplicates == 0:
        return True, ''
    return False, f'want 0 duplicate rows, got {num_duplicates}'


# DataFrame column level checks are described in functions using
# the naming convention colcheck_[some name](df: pd.DatFrame,
# col_name: str, [inputs]) -> Tuple[bool, str].
# The return value is a tuple containing a bool indicating if the
# test passed or failed (true = passed) and a string describing
# the error condition if the test failed. Error messages follow
# the pattern 'column [column name] want [expected value or
# condition], got [actual value or condition]'.


def colcheck_exists(df: pd.DataFrame, col_name: str) -> Tuple[bool, str]:
    '''Check if a column with the specified name exists in the dataset.'''
    if col_name in df.columns:
        return True, ''
    return False, f'column {col_name} not found in data'


def colcheck_count_distinct(df: pd.DataFrame, col_name: str, count: int,
                            operator: str = '==') -> Tuple[bool, str]:
    '''
    Check if the count of distinct values in a column is equal to, greater
    than or less than a specified count.

    The operator parameter can be '==', '>=' or '<='.
    '''
    count_val = df[col_name].nunique()
    if operator == '==' and count_val == count:
        return True, ''
    if operator == '>=' and count_val >= count:
        return True, ''
    if operator == '<=' and count_val <= count:
        return True, ''
    if operator not in ['==', '<=', '>=']:
        return False, (f'column {col_name} count distinct '
                       f'operator {operator} not recognised')
    return False, (f'column {col_name} want count distinct {operator} '
                   f'{count}, got {count_val}')


def colcheck_is_numeric(df: pd.DataFrame, col_name: str) -> Tuple[bool, str]:
    '''Check if a column is numeric.'''
    if pd.api.types.is_numeric_dtype(df[col_name]):
        return True, ''
    return False, f'column {col_name} expected to be numeric but is not'


def colcheck_is_str(df: pd.DataFrame, col_name: str) -> Tuple[bool, str]:
    '''Check if a column is string type.'''
    if pd.api.types.is_string_dtype(df[col_name]):
        return True, ''
    return False, f'column {col_name} expected to be string type but is not'


def colcheck_min_val(df: pd.DataFrame,
                     col_name: str,
                     min_val: float) -> Tuple[bool, str]:
    '''Check if a column has a value less than a minimum value.'''
    actual_min = df[col_name].min()
    if actual_min >= min_val:
        return True, ''
    return False, (f'column {col_name} '
                   f'want {min_val} minimum value, '
                   f'got {actual_min}')


def colcheck_no_nulls(df: pd.DataFrame, col_name: str) -> Tuple[bool, str]:
    '''Check if a column contains null values.'''
    countnull = pd.isnull(df[col_name]).sum()
    if countnull == 0:
        return True, ''
    return False, f'column {col_name} want 0 nulls, got {countnull}'
