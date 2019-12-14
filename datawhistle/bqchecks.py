import subprocess
import json
from typing import Tuple, Union, Optional


# Note this is defined as a list because that is how the subprocess.run
# command wants it.
BQ_QUERY = ['bq', 'query', '--nouse_legacy_sql', '--format=json',
            '--quiet=true']

# Check if a column exists in the dataset schema, without returning an
# empty result if the column doesn't exist.
SQL_COL_EXISTS = '''WITH query1 AS
  (SELECT "True" AS bool
   FROM {datasetname}.INFORMATION_SCHEMA.COLUMNS
   WHERE table_name = "{tablename}" AND column_name = "{columnname}")
SELECT * FROM query1
UNION ALL
SELECT "False" AS bool FROM (SELECT 1)
LEFT JOIN query1 ON FALSE WHERE NOT EXISTS (SELECT 1 FROM query1);
'''

# Count the distinct values in a column.
SQL_COUNTDISTINCT = '''SELECT COUNT(DISTINCT {columnname}) AS number
FROM {datasetname}.{tablename};
'''

# Count instances where column value is not equal to a specified
# value.
SQL_COUNTNOT_EQ = '''SELECT SUM(flags) AS number
FROM (SELECT CASE WHEN {columnname} = {value} THEN 0 ELSE 1 END AS flags
      FROM {datasetname}.{tablename});
'''

# Get the maximum value in a column.
SQL_COL_MAX = '''SELECT MAX({columnname}) AS number
FROM {datasetname}.{tablename};
'''

# Get the minimum value in a column.
SQL_COL_MIN = '''SELECT MIN({columnname}) AS number
FROM {datasetname}.{tablename};
'''

# Get column's type, without returning an empty result if the column does
# not exist.
SQL_COL_TYPE = '''WITH query1 AS
  (SELECT data_type AS string
   FROM {datasetname}.INFORMATION_SCHEMA.COLUMNS
   WHERE table_name = "{tablename}" AND column_name="{columnname}")
SELECT * FROM query1
UNION ALL
SELECT "__no_data__" AS string FROM (SELECT 1)
LEFT JOIN query1 ON FALSE WHERE NOT EXISTS (SELECT 1 FROM query1);
'''

# Count the number of values outside 1.5 times the inter quartile
# range in a column.
SQL_COUNTOUTLIERS = '''DECLARE q25 FLOAT64;
DECLARE q75 FLOAT64;
DECLARE IQRX FLOAT64;
SET (q25, q75) = (
  SELECT AS STRUCT percentiles[offset(25)] AS q25,
                   percentiles[offset(75)] AS q75
  FROM (SELECT APPROX_QUANTILES({columnname}, 100) percentiles
        FROM {datasetname}.{tablename}));
SET IQRX = 1.5 * (q75 - q25);
WITH query1 AS
  (SELECT CASE WHEN {columnname} < (q25 - IQRX) THEN 1
               WHEN {columnname} > (q75 + IQRX) THEN 1
               ELSE 0 END AS flag
   FROM {datasetname}.{tablename})
SELECT sum(flag) AS number FROM query1;
'''

# Count the number of blank (whitespace) string values in a column.
SQL_COUNTBLANKS = '''SELECT SUM(flag) as number
FROM (SELECT CASE WHEN TRIM({columnname}) = ""
                  THEN 1 ELSE 0
             END AS flag
      FROM {datasetname}.{tablename});
'''

# Count the number of duplicate values in a column.
SQL_COUNTDUPLICATES = '''SELECT SUM(count) AS number
FROM (SELECT {columnname} AS rowvalue,
      CASE WHEN COUNT(*) > 1 THEN 1 ELSE 0 END AS count
      FROM {datasetname}.{tablename} GROUP BY {columnname});
'''

# Count the number of null values in a column.
SQL_COUNTNULLS = '''SELECT SUM(number) AS number
FROM (SELECT CASE WHEN {columnname} IS NULL THEN 1 ELSE 0 END AS number
      FROM {datasetname}.{tablename});
'''

# Check a specific regex match on a column
SQL_COUNTREGEX = '''SELECT MATCHES/COL_COUNT as number
FROM (SELECT
  SUM(CASE WHEN REGEXP_CONTAINS({columnname}, r"{regex_rule}") THEN 1 ELSE 0 END) AS MATCHES,
  COUNT({columnname}) AS COL_COUNT
FROM {datasetname}.{tablename})'''

# Count the number of rows in a table.
SQL_COUNTROWS = 'SELECT count(*) AS number FROM {datasetname}.{tablename};'

# Check if a table exists in the dataset schema, without returning an empty
# result if the table doesn't exist.
SQL_TABLE_EXISTS = '''WITH query1 AS
  (SELECT "True" AS bool
   FROM {datasetname}.INFORMATION_SCHEMA.TABLES
   WHERE table_name = "{tablename}")
SELECT * FROM query1
UNION ALL
SELECT "False" AS bool FROM (SELECT 1)
LEFT JOIN query1 ON FALSE WHERE NOT EXISTS (SELECT 1 FROM query1);
'''


class BqError(Exception):
    pass


def _bqquery_get_number(query: str) -> float:
    jsontxt = _bqquery_run(query)
    jsondict = json.loads(jsontxt)
    if len(jsondict) == 0:
        raise BqError('Could not convert bq command output')
    jsondict = jsondict[0]
    # SQL_COUNTOUTLIERS returns an extra list wrapping.
    if isinstance(jsondict, list) and len(jsondict) > 0:
        jsondict = jsondict[0]
    if not isinstance(jsondict, dict):
        raise BqError('Could not convert bq command output')
    if 'number' not in jsondict.keys():
        raise BqError('Could not convert bq command output')
    try:
        return float(jsondict['number'])
    except ValueError:
        raise BqError('Could not convert bq command output')


def _bqquery_get_string(query: str) -> str:
    jsontxt = _bqquery_run(query)
    jsondict = json.loads(jsontxt)
    if len(jsondict) == 0:
        raise BqError('Could not convert bq command output')
    jsondict = jsondict[0]
    if not isinstance(jsondict, dict):
        raise BqError('Could not convert bq command output')
    if 'string' not in jsondict.keys():
        raise BqError('Could not convert bq command output')
    return jsondict['string']


def _bqquery_get_bool(query: str) -> bool:
    jsontxt = _bqquery_run(query)
    jsondict = json.loads(jsontxt)
    if len(jsondict) == 0:
        raise BqError('Could not convert bq command output')
    jsondict = jsondict[0]
    if not isinstance(jsondict, dict):
        raise BqError('Could not convert bq command output')
    if 'bool' not in jsondict.keys():
        raise BqError('Could not convert bq command output')
    return jsondict['bool'] == 'True'


def _bqquery_run(query: str) -> str:
    bqcommand = BQ_QUERY.copy()
    bqcommand.append(query)
    result = subprocess.run(bqcommand, capture_output=True, text=True)
    if result.returncode != 0:
        raise BqError((f'Error executing bq command: {result.stdout} '
                       f'{result.stderr}'))
    return result.stdout


# Table level checks (as opposed to column level checks)
# are described in functions using the naming convention
# dscheck_[some name](datasetname: str, tablename: str,
# [inputs]) -> Tuple[bool, str].
# The return value is a tuple containing a bool indicating if the
# test passed or failed (true = passed) and a string describing
# the error condition if the test failed. Error messages follow
# the pattern 'want [expected value or condition], got [actual
# value or condition]'.


def dscheck_row_count(datasetname: str, tablename: str, count: int,
                      operator: str = '==') -> Tuple[bool, str]:
    '''
    Check if the number of rows in a table is equal to, greater
    than or less than a specified count.

    The operator parameter can be '==', '>=' or '<='.
    '''
    sql = SQL_COUNTROWS.format(datasetname=datasetname, tablename=tablename)
    num_rows: float = _bqquery_get_number(sql)
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


def dscheck_table_exists(datasetname: str, tablename: str) -> Tuple[bool, str]:
    '''Check if a table exists in the specified dataset.'''
    sql = SQL_TABLE_EXISTS.format(datasetname=datasetname, tablename=tablename)
    table_exists: bool = _bqquery_get_bool(sql)
    if table_exists:
        return True, ''
    return False, f'table {tablename} not found in dataset {datasetname}'


# Table column level checks are described in functions using
# the naming convention
# colcheck_[some name](datasetname: str, tablename: str,
# [inputs]) -> Tuple[bool, str].
# The return value is a tuple containing a bool indicating if the
# test passed or failed (true = passed) and a string describing
# the error condition if the test failed. Error messages follow
# the pattern 'column [column name] want [expected value or
# condition], got [actual value or condition]'.


def colcheck_exists(datasetname: str, tablename: str,
                    columnname: str) -> Tuple[bool, str]:
    '''Check if a column with the specified name exists in the table.'''
    sql = SQL_COL_EXISTS.format(datasetname=datasetname, tablename=tablename,
                                columnname=columnname)
    col_exists: bool = _bqquery_get_bool(sql)
    if col_exists:
        return True, ''
    return False, f'column {columnname} not found in table {tablename}'


def colcheck_count_distinct(datasetname: str, tablename: str,
                            columnname: str, count: int,
                            operator: str = '==') -> Tuple[bool, str]:
    '''
    Check if the count of distinct values in a column is equal to, greater
    than or less than a specified count.

    The operator parameter can be '==', '>=' or '<='.
    '''
    sql = SQL_COUNTDISTINCT.format(datasetname=datasetname,
                                   tablename=tablename,
                                   columnname=columnname)
    count_val = _bqquery_get_number(sql)
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


def colcheck_is_numeric(datasetname: str, tablename: str,
                        columnname: str) -> Tuple[bool, str]:
    '''Check if a column is numeric.'''
    sql = SQL_COL_TYPE.format(datasetname=datasetname, tablename=tablename,
                              columnname=columnname)
    coltype = _bqquery_get_string(sql)
    if coltype in ['INT64', 'NUMERIC', 'FLOAT64']:
        return True, ''
    return False, f'column {columnname} want numeric type, got {coltype}'


def colcheck_is_str(datasetname: str, tablename: str,
                    columnname: str) -> Tuple[bool, str]:
    '''Check if a column is string type.'''
    sql = SQL_COL_TYPE.format(datasetname=datasetname, tablename=tablename,
                              columnname=columnname)
    coltype = _bqquery_get_string(sql)
    if coltype == 'STRING':
        return True, ''
    return False, f'column {columnname} want string type, got {coltype}'


def colcheck_iqr(datasetname: str, tablename: str,
                 columnname: str) -> Tuple[bool, str]:
    '''
    Check if the values in a column are outliers greater than or less than
    1.5 times the inter-quartile range plus Q3 or Q1 respectively
    '''
    query = SQL_COUNTOUTLIERS.format(datasetname=datasetname,
                                     tablename=tablename,
                                     columnname=columnname)
    outliercount = _bqquery_get_number(query)
    if outliercount == 0:
        return True, ''
    return False, f'column {columnname} want 0 outliers, got {outliercount}'


def colcheck_is_datetime(datasetname: str, tablename: str,
                         columnname: str) -> Tuple[bool, str]:
    '''Check if a column is datetime type.'''
    sql = SQL_COL_TYPE.format(datasetname=datasetname, tablename=tablename,
                              columnname=columnname)
    coltype = _bqquery_get_string(sql)
    if coltype in ['DATE', 'DATETIME']:
        return True, ''
    return False, f'column {columnname} want datetime type, got {coltype}'


def colcheck_no_blanks(datasetname: str, tablename: str,
                       columnname: str) -> Tuple[bool, str]:
    '''Check if a string column contains blanks or whitespace only values.'''
    sql = SQL_COUNTBLANKS.format(datasetname=datasetname, tablename=tablename,
                                 columnname=columnname)
    count = _bqquery_get_number(sql)
    if count == 0:
        return True, ''
    return False, f'column {columnname} want no blanks, got {count}'


def colcheck_no_duplicates(datasetname: str, tablename: str,
                           columnname: str) -> Tuple[bool, str]:
    '''Check that a column doesn't contain any duplicates.'''
    sql = SQL_COUNTDUPLICATES.format(datasetname=datasetname,
                                     tablename=tablename,
                                     columnname=columnname)
    num_duplicates = _bqquery_get_number(sql)
    if num_duplicates == 0:
        return True, ''
    return False, (f'column {columnname} want 0 duplicate rows, '
                   f'got {num_duplicates}')


def colcheck_no_nulls(datasetname: str, tablename: str,
                      columnname: str) -> Tuple[bool, str]:
    '''Check if a column contains null values.'''
    sql = SQL_COUNTNULLS.format(datasetname=datasetname,
                                tablename=tablename,
                                columnname=columnname)
    countnull = _bqquery_get_number(sql)
    if countnull == 0:
        return True, ''
    return False, f'column {columnname} want 0 nulls, got {countnull}'


def colcheck_regex(datasetname: str, tablename: str,
                      columnname: str, regex_rule: Optional[str], regex_type: Optional[str]) -> Tuple[bool, str]:
    '''Check to see if a column contains all the same regex type, or if the column does
    not contain a regex type.'''

    if regex_rule is None or regex_type is None:
        return False, f'column {columnname} None regex_rule or regex_type'

    if regex_rule == '':
        return False, f'column {columnname} blank regex_rule'

    try:
        sql = SQL_COUNTREGEX.format(datasetname=datasetname,
                                tablename=tablename,
                                columnname=columnname,
                                regex_rule=regex_rule)
        row_fraction_match = _bqquery_get_number(sql)
    except BqError:
        return False, f'column {columnname} BqError with rule {regex_rule}'

    if regex_type == 'mandatory' and row_fraction_match < 1:
        return False, f'column {columnname} found a non matching regex record with rule {regex_rule}'
    elif regex_type == 'exclude' and row_fraction_match > 0:
        return False, f'column {columnname} found invalid regex with rule {regex_rule}'
    return True, ''

def colcheck_val(datasetname: str, tablename: str,
                 columnname: str, val: Union[int, float],
                 operator: str = '==') -> Tuple[bool, str]:
    '''
    Check if the values in a column are equal to, greater than or less than
    a specified value.

    The operator parameter can be '==', '>=' or '<='.
    '''
    if operator not in ['==', '<=', '>=']:
        return False, (f'column {columnname} value check '
                       f'operator {operator} not recognised')
    if operator == '<=':
        sql = SQL_COL_MAX.format(datasetname=datasetname, tablename=tablename,
                                 columnname=columnname)
        actual_val = _bqquery_get_number(sql)
        if actual_val <= val:
            return True, ''
    if operator == '>=':
        sql = SQL_COL_MIN.format(datasetname=datasetname, tablename=tablename,
                                 columnname=columnname)
        actual_val = _bqquery_get_number(sql)
        if actual_val >= val:
            return True, ''
    if operator == '==':
        sql = SQL_COUNTNOT_EQ.format(datasetname=datasetname,
                                     tablename=tablename,
                                     columnname=columnname,
                                     value=val)
        count = _bqquery_get_number(sql)
        if count == 0:
            return True, ''
        actual_val = f'{count} not'
    return False, (f'column {columnname} want value {operator} '
                   f'{val}, got {actual_val}')
