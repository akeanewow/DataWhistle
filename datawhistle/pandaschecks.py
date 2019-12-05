from typing import Tuple, Union
import pandas as pd  # type: ignore


# TODO: refactor col_name to columnname to be consistent with
# bqchecks.py. Also col_type to columntype.

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
    Check if the number of rows in a table is equal to, greater
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
        return False, (f'table row count '
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
    '''Check if a column with the specified name exists in the table.'''
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


def colcheck_is_datetime(df: pd.DataFrame, col_name: str, format: str = None) -> Tuple[bool, str]:
    '''Check if a column is datetime type,  format.'''


    if format is not None:
        try:
            df[col_name] = pd.to_datetime(df[col_name], format=format)
        except ValueError:
            return False, f'column {col_name} data does not match datetime format specified'
        except Exception as ex:
            return False, f'column {col_name} expected to be datetime type but is not'
    else:
        try:
            df[col_name] = pd.to_datetime(df[col_name])
        except Exception as ex:
            return False, f'column {col_name} expected to be datetime type but is not'

    if pd.api.types.is_datetime64_dtype(df[col_name]):
        return True, ''
    return False, f'column {col_name} expected to be datetime type but is not'


def colcheck_no_blanks(df: pd.DataFrame, col_name: str) -> Tuple[bool, str]:
    '''Check if a string column contains blanks or whitespace only values.'''
    err = f'column {col_name} has blanks or whitesplace only values'
    if df[col_name].str.isspace().sum() > 0:
        return False, err
    if sum(df[col_name] == '') == 0:
        return True, ''
    return False, err


def colcheck_no_duplicates(df: pd.DataFrame,
                           col_name: str) -> Tuple[bool, str]:
    '''Check that a column doesn't contain any duplicates.'''
    num_duplicates: int = sum(df[col_name].duplicated())
    if num_duplicates == 0:
        return True, ''
    return False, (f'column {col_name} want 0 duplicate rows, '
                   f'got {num_duplicates}')


def colcheck_no_nulls(df: pd.DataFrame, col_name: str) -> Tuple[bool, str]:
    '''Check if a column contains null values.'''
    countnull = pd.isnull(df[col_name]).sum()
    if countnull == 0:
        return True, ''
    return False, f'column {col_name} want 0 nulls, got {countnull}'


def colcheck_val(df: pd.DataFrame, col_name: str, val: Union[int, float],
                 operator: str = '==') -> Tuple[bool, str]:
    '''
    Check if the values in a column are equal to, greater than or less than
    a specified value.

    The operator parameter can be '==', '>=' or '<='.
    '''
    if operator == '==':
        if sum(df[col_name] == val) == len(df):
            return True, ''
        else:
            return False, (f'column {col_name} want all values = {val}, '
                           f'got different values')
    if operator == '>=':
        actual_val = df[col_name].min()
        if actual_val >= val:
            return True, ''
    if operator == '<=':
        actual_val = df[col_name].max()
        if actual_val <= val:
            return True, ''
    if operator not in ['==', '<=', '>=']:
        return False, (f'column {col_name} value check '
                       f'operator {operator} not recognised')
    return False, (f'column {col_name} want value {operator} '
                   f'{val}, got {actual_val}')
