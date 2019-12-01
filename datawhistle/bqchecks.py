import subprocess
import json
from typing import Tuple


# Note this is defined as a list because that is how the subprocess.run
# command wants it.
BQ_QUERY = ['bq', 'query', '--nouse_legacy_sql', '--format=json',
            '--quiet=true']

# Get the column type (longer than would be expected to return "__no_data__"
# instead of nothing if the column does not exist, to know with certainty
# that a JSON parsing error hasn't occurred in the _bqquery_get_string
# function.
SQL_COLTYPE = '''WITH query1 AS
  (SELECT data_type AS string
   FROM {datasetname}.INFORMATION_SCHEMA.COLUMNS
   WHERE table_name = "{tablename}" AND column_name="{columnname}")
SELECT * FROM query1
UNION ALL
SELECT "__no_data__" AS string FROM (SELECT 1)
LEFT JOIN query1 ON FALSE WHERE NOT EXISTS (SELECT 1 FROM query1);
'''

# Get the number of columns in a table.
SQL_COUNTCOLS = '''SELECT count(*) as number
FROM {datasetname}.INFORMATION_SCHEMA.COLUMNS
WHERE table_name = '{tablename}';'''

# Count the number of rows in a table.
SQL_COUNTROWS = 'SELECT count(*) AS number FROM {datasetname}.{tablename};'


class BqError(Exception):
    pass


def _bqquery_get_number(query: str) -> float:
    jsontxt = _bqquery_run(query)
    jsondict = json.loads(jsontxt)
    if len(jsondict) == 0:
        raise BqError('Could not convert bq command output')
    jsondict = jsondict[0]
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
    if 'string' not in jsondict.keys():
        raise BqError('Could not convert bq command output')
    return jsondict['string']


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


# Table column level checks are described in functions using
# the naming convention
# colcheck_[some name](datasetname: str, tablename: str,
# [inputs]) -> Tuple[bool, str].
# The return value is a tuple containing a bool indicating if the
# test passed or failed (true = passed) and a string describing
# the error condition if the test failed. Error messages follow
# the pattern 'column [column name] want [expected value or
# condition], got [actual value or condition]'.


# To be converted:
# def colcheck_exists(df: pd.DataFrame, col_name: str) -> Tuple[bool, str]:
#    '''Check if a column with the specified name exists in the dataset.'''
#    if col_name in df.columns:
#        return True, ''
#    return False, f'column {col_name} not found in data'
