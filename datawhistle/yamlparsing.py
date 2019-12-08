import yaml  # type: ignore
from typing import Any, Dict, List
import datawhistle as dw


YAML_TOPLEVEL_KEYS = ['table', 'columns']
YAML_TABLE_KEYS = [
    'stop_on_fail',
    'allow_duplicate_rows',
    'row_count_max',
    'row_count_min',
    'row_count']
YAML_COLUMN_KEYS = [
    'name',
    'type',
    'allow_blanks',
    'allow_duplicates',
    'allow_nulls',
    'count_distinct_max',
    'count_distinct_min',
    'count_distinct',
    'dateformat',
    'min',
    'max',
    'val',
    'regex_rule']
YAML_COLUMN_TYPES = ['numeric', 'string', 'datetime']
TRUE_VALS = [True, 1, 'true', 'True', '1']
FALSE_VALS = [False, 0, 'false', 'False', '0']


class YamlParsingError(Exception):
    pass


def _check_bool_val(val: Any) -> bool:
    if val in TRUE_VALS:
        return True
    if val not in FALSE_VALS:
        raise YamlParsingError(f'want boolean value, got {val}')
    return False


def _check_yaml_column_keys(colkeys: List[str]) -> None:
    if 'name' not in colkeys:
        raise YamlParsingError('column name missing')
    if 'type' not in colkeys:
        raise YamlParsingError('column type missing')
    for key in colkeys:
        if key not in YAML_COLUMN_KEYS:
            raise YamlParsingError(f'unexpected column attribute: {key}')


def _check_yaml_column_type(coltype: str) -> None:
    if coltype not in YAML_COLUMN_TYPES:
        raise YamlParsingError(f'column type {coltype} not recognised')


def _check_yaml_toplevel_keys(ykeys: List[str]) -> None:
    for key in ykeys:
        if key not in YAML_TOPLEVEL_KEYS:
            raise YamlParsingError(f'unexpected yaml attribute: {key}')


def _check_yaml_table_keys(dsdictkeys: List[str]) -> None:
    for key in dsdictkeys:
        if key not in YAML_TABLE_KEYS:
            raise YamlParsingError(f'unexpected table attribute: {key}')


def _yamlerr(message: str) -> None:
    raise YamlParsingError(message)


def apply_yamldict_to_checksuite(ymld: Dict,
                                 suite: dw.PandasDatsetCheckSuite) -> None:
    '''Apply yaml parsed into dictionary to a checksuite object.'''
    ykeys = list(ymld.keys())
    _check_yaml_toplevel_keys(ykeys)
    #
    # Process table
    if 'table' in ykeys:
        dsdict = ymld['table']
        dsdictkeys = list(dsdict.keys())
        _check_yaml_table_keys(dsdictkeys)
        # stop on first check fail
        if 'stop_on_fail' in dsdictkeys:
            suite.stop_on_fail = _check_bool_val(dsdict['stop_on_fail'])
        # allow duplicate rows
        dups = 'allow_duplicate_rows'
        if dups in dsdictkeys:
            suite.allow_duplicate_rows = _check_bool_val(dsdict[dups])
        #  maximum number of rows
        if 'row_count_max' in dsdictkeys:
            val = dsdict['row_count_max']
            if not isinstance(val, int):
                _yamlerr((f'table: row_count_max want an integer, '
                          f'got {val}({type(val)})'))
            suite.row_count_max = val
        #  minimum number of rows
        if 'row_count_min' in dsdictkeys:
            val = dsdict['row_count_min']
            if not isinstance(val, int):
                _yamlerr((f'table: row_count_min want an integer, '
                          f'got {val}({type(val)})'))
            suite.row_count_min = val
        #  number of rows
        if 'row_count' in dsdictkeys:
            val = dsdict['row_count']
            if not isinstance(val, int):
                _yamlerr((f'table: row_count want an integer, '
                          f'got {val}({type(val)})'))
            suite.row_count = val
    #
    # Process columns
    if 'columns' not in ykeys:
        return
    colslist = ymld['columns']
    for coldict in colslist:
        colkeys = list(coldict.keys())
        _check_yaml_column_keys(colkeys)
        colname = coldict['name']
        coltype = coldict['type']
        _check_yaml_column_type(coltype)
        col = suite.addcolumn(colname, coltype)
        # allow blanks in the column
        if 'allow_blanks' in colkeys:
            col.allow_blanks = _check_bool_val(coldict['allow_blanks'])
        # allow null values in the column
        if 'allow_nulls' in colkeys:
            col.allow_nulls = _check_bool_val(coldict['allow_nulls'])
        # duplicate rows
        if 'allow_duplicates' in colkeys:
            col.allow_duplicates = _check_bool_val(coldict['allow_duplicates'])
        # count distinct checks
        if 'count_distinct_max' in colkeys:
            val = coldict['count_distinct_max']
            if not isinstance(val, int):
                _yamlerr(f'column {colname} count_distinct_max error {val}')
            col.count_distinct_max = val
        if 'count_distinct_min' in colkeys:
            val = coldict['count_distinct_min']
            if not isinstance(val, int):
                _yamlerr(f'column {colname} count_distinct_min error {val}')
            col.count_distinct_min = val
        if 'count_distinct' in colkeys:
            val = coldict['count_distinct']
            if not isinstance(val, int):
                _yamlerr(f'column {colname} count_distinct error {val}')
            col.count_distinct = val
        if 'dateformat' in colkeys:
            val = coldict['dateformat']
            if not isinstance(val, str):
                _yamlerr(f'column {colname} format error {val}')
            col.dateformat = val
        # column value checks
        if 'min' in colkeys:
            val = coldict['min']
            if (not isinstance(val, int)) and (not isinstance(val, float)):
                _yamlerr(f'column {colname} cannot check minimum value of non '
                         f'numeric column')
            col.min_val = val
        if 'max' in colkeys:
            val = coldict['max']
            if (not isinstance(val, int)) and (not isinstance(val, float)):
                _yamlerr(f'column {colname} cannot check maximum value of non '
                         f'numeric column')
            col.max_val = val
        if 'val' in colkeys:
            val = coldict['val']
            if (not isinstance(val, int)) and (not isinstance(val, float)):
                _yamlerr(f'column {colname} cannot check value of non '
                         f'numeric column')
            col.val = val
        if 'regex_rule' in colkeys:
            val = coldict['regex_rule']
            if not isinstance(val, str):
                _yamlerr(f'column {colname} format error {val}')
            elif coltype != 'string':
                _yamlerr(f'column {colname} is of type {coltype}, but must be of type string for regex_rules')
            col.regex_rule = val


def load_yaml_file_to_dict(filename: str) -> Dict:
    '''Parse a yaml file into a Dict object.'''
    with open(filename, 'r') as stream:
        parsed = yaml.safe_load(stream)
    if not isinstance(parsed, dict):
        raise YamlParsingError(f'error converting YAML markup in {filename}')
    return parsed
