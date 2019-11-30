import subprocess
import json
from typing import Tuple


BQ_QUERY = ['bq', 'query', '--format=json', '--quiet=true']

SQL_COUNTROWS = 'SELECT count(*) as number FROM {datasetname}.{tablename};'


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
# bqcheck_[some name](datasetname: str, tablename: str,
# [inputs]) -> Tuple[bool, str].
# The return value is a tuple containing a bool indicating if the
# test passed or failed (true = passed) and a string describing
# the error condition if the test failed. Error messages follow
# the pattern 'want [expected value or condition], got [actual
# value or condition]'.


def bqcheck_row_count(datasetname: str, tablename: str, count: int,
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
