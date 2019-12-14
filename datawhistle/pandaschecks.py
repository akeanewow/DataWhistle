from typing import Optional, Tuple, Union
import pandas as pd     # type: ignore
import numpy as np      # type: ignore
import re

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
# columnname: str, [inputs]) -> Tuple[bool, str].
# The return value is a tuple containing a bool indicating if the
# test passed or failed (true = passed) and a string describing
# the error condition if the test failed. Error messages follow
# the pattern 'column [column name] want [expected value or
# condition], got [actual value or condition]'.


def colcheck_exists(df: pd.DataFrame, columnname: str) -> Tuple[bool, str]:
    '''Check if a column with the specified name exists in the table.'''
    if columnname in df.columns:
        return True, ''
    return False, f'column {columnname} not found in data'


def colcheck_count_distinct(df: pd.DataFrame, columnname: str, count: int,
                            operator: str = '==') -> Tuple[bool, str]:
    '''
    Check if the count of distinct values in a column is equal to, greater
    than or less than a specified count.

    The operator parameter can be '==', '>=' or '<='.
    '''
    count_val = df[columnname].nunique()
    if operator == '==' and count_val == count:
        return True, ''
    if operator == '>=' and count_val >= count:
        return True, ''
    if operator == '<=' and count_val <= count:
        return True, ''
    if operator not in ['==', '<=', '>=']:
        return False, (f'column {columnname} count distinct '
                       f'operator {operator} not recognised')
    return False, (f'column {columnname} want count distinct {operator} '
                   f'{count}, got {count_val}')


def colcheck_is_numeric(df: pd.DataFrame, columnname: str) -> Tuple[bool, str]:
    '''Check if a column is numeric.'''
    if pd.api.types.is_numeric_dtype(df[columnname]):
        return True, ''
    return False, f'column {columnname} expected to be numeric but is not'


def colcheck_is_str(df: pd.DataFrame, columnname: str) -> Tuple[bool, str]:
    '''Check if a column is string type.'''
    if pd.api.types.is_string_dtype(df[columnname]):
        return True, ''
    return False, f'column {columnname} expected to be string type but is not'


def colcheck_is_datetime(df: pd.DataFrame, columnname: str,
                         dateformat: Optional[str] = None) -> Tuple[bool, str]:
    '''
    Check if a column is datetime, optionally using a datetime format
    format string.
    '''
    if dateformat is not None:
        try:
            df[columnname] = pd.to_datetime(df[columnname], format=dateformat,
                                            exact=True)
            return True, ''
        except ValueError:
            return False, (f'column {columnname} data does not match datetime '
                           f'format {dateformat}')
        except Exception:
            return False, (f'column {columnname} expected to be datetime type '
                           'but is not')
    else:
        try:
            df[columnname] = pd.to_datetime(df[columnname])
            return True, ''
        except Exception:
            return False, (f'column {columnname} expected to be datetime type '
                           'but is not')
    return False, (f'column {columnname} expected to be datetime type '
                   'but is not')


def colcheck_no_blanks(df: pd.DataFrame, columnname: str) -> Tuple[bool, str]:
    '''Check if a string column contains blanks or whitespace only values.'''
    err = f'column {columnname} has blanks or whitesplace only values'
    if df[columnname].str.isspace().sum() > 0:
        return False, err
    if sum(df[columnname] == '') == 0:
        return True, ''
    return False, err


def colcheck_no_duplicates(df: pd.DataFrame,
                           columnname: str) -> Tuple[bool, str]:
    '''Check that a column doesn't contain any duplicates.'''
    num_duplicates: int = sum(df[columnname].duplicated())
    if num_duplicates == 0:
        return True, ''
    return False, (f'column {columnname} want 0 duplicate rows, '
                   f'got {num_duplicates}')


def colcheck_no_nulls(df: pd.DataFrame, columnname: str) -> Tuple[bool, str]:
    '''Check if a column contains null values.'''
    countnull = pd.isnull(df[columnname]).sum()
    if countnull == 0:
        return True, ''
    return False, f'column {columnname} want 0 nulls, got {countnull}'


def colcheck_regex(df: pd.DataFrame, columnname: str,
                   regex_rule: Optional[str],
                   regex_type: Optional[str]) -> Tuple[bool, str]:
    '''
    Check to see if a column contains all the same regex type, or if the
    column does not contain a regex type.
    '''
    if regex_rule is None or regex_type is None:
        return False, f'column {columnname} None regex_rule or regex_type'
    if regex_rule == '':
        return False, f'column {columnname} blank regex_rule'
    try:
        reg_results = df[columnname].str.findall(regex_rule)
    except re.error:
        return False, f'column {columnname} invalid regex_rule {regex_rule}'
    for row in reg_results.values:
        if row == [''] or row == []:
            # Not found
            if regex_type == 'mandatory':
                return False, (f'column {columnname} found a non matching '
                               f'regex record with rule {regex_rule}')
        else:
            # Found
            if regex_type == 'exclude':
                return False, (f'column {columnname} found invalid regex '
                               f'{row[0]} with rule {regex_rule}')
    return True, ''


def colcheck_val(df: pd.DataFrame, columnname: str, val: Union[int, float],
                 operator: str = '==') -> Tuple[bool, str]:
    '''
    Check if the values in a column are equal to, greater than or less than
    a specified value.

    The operator parameter can be '==', '>=' or '<='.
    '''
    if operator not in ['==', '<=', '>=']:
        return False, (f'column {columnname} value check '
                       f'operator {operator} not recognised')
    if operator == '==':
        if sum(df[columnname] == val) == len(df):
            return True, ''
        else:
            return False, (f'column {columnname} want all values = {val}, '
                           f'got different values')
    if operator == '>=':
        actual_val = df[columnname].min()
        if actual_val >= val:
            return True, ''
    if operator == '<=':
        actual_val = df[columnname].max()
        if actual_val <= val:
            return True, ''
    return False, (f'column {columnname} want value {operator} '
                   f'{val}, got {actual_val}')


def colcheck_iqr(df: pd.DataFrame, columnname: str) -> Tuple[bool, str]:
    '''
    Check if the values in a column are outliers greater than or less than
    1.5 times the inter-quartile range plus Q3 or Q1 respectively
    '''
    q25, q75 = np.percentile(df[columnname], [25, 75])
    upper = round(q75 + (q75 - q25) * 1.5, 2)
    lower = round(q25 - (q75 - q25) * 1.5, 2)
    if max(df[columnname]) > upper:
        return False, (f'column {columnname} outlier above 1.5xIQR {upper}: '
                       f'{max(df[columnname])}')
    if min(df[columnname]) < lower:
        return False, (f'column {columnname} outlier below 1.5xIQR {lower}: '
                       f' {min(df[columnname])}')
    return True, ''
