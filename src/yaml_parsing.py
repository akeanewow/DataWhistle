import yaml  # type: ignore
from typing import Any, Dict, List
import checksuites as cs


_YAML_TOPLEVEL_KEYS = ['dataset', 'columns']
_YAML_DATASET_KEYS = ['stop_on_fail', 'allow_duplicate_rows', 'min_rows']
_YAML_COLUMN_KEYS = ['name', 'type']
_YAML_COLUMN_TYPES = ['numeric', 'string']

_TRUE_VALS = [True, 1, 'true', 'True', '1']
_FALSE_VALS = [False, 0, 'false', 'False', '0']


class YamlParsingError(Exception):
    pass


def load_yaml_file_to_dict(filename: str) -> Dict:
    '''Parse a yaml file into a Dict object.'''
    with open(filename, 'r') as stream:
        parsed = yaml.safe_load(stream)
    if not isinstance(parsed, dict):
        raise YamlParsingError(f'error converting YAML markup in {filename}')
    return parsed


def _checktoplevelkeys(ykeys: List[str]) -> None:
    for key in ykeys:
        if key not in _YAML_TOPLEVEL_KEYS:
            raise YamlParsingError(f'unexpected yaml attribute: {key}')


def _checkdatasetkeys(dsdictkeys: List[str]) -> None:
    for key in dsdictkeys:
        if key not in _YAML_DATASET_KEYS:
            raise YamlParsingError(f'unexpected dataset attribute: {key}')


def _checkcolumnkeys(colkeys: List[str]) -> None:
    if 'name' not in colkeys:
        raise YamlParsingError('column name missing')
    if 'type' not in colkeys:
        raise YamlParsingError('column type missing')
    for key in colkeys:
        if key not in _YAML_COLUMN_KEYS:
            raise YamlParsingError(f'unexpected column attribute: {key}')


def _checkcolumntype(coltype: str) -> None:
    if coltype not in _YAML_COLUMN_TYPES:
        raise YamlParsingError(f'column type {coltype} not recognised')


def _check_bool_val(val: Any) -> bool:
    if val in _TRUE_VALS:
        return True
    if val not in _FALSE_VALS:
        raise YamlParsingError(f'want boolean value, got {val}')
    return False


def apply_yamldict_to_checksuite(ymld: Dict,
                                 suite: cs.PandasDatsetCheckSuite) -> None:
    '''Apply yaml parsed into dictionary to a checksuite object.'''
    ykeys = list(ymld.keys())
    _checktoplevelkeys(ykeys)
    if 'dataset' in ykeys:
        dsdict = ymld['dataset']
        dsdictkeys = list(dsdict.keys())
        _checkdatasetkeys(dsdictkeys)
        if 'stop_on_fail' in dsdictkeys:
            suite.stop_on_fail = _check_bool_val(dsdict['stop_on_fail'])
        dups = 'allow_duplicate_rows'
        if dups in dsdictkeys:
            suite.allow_duplicate_rows = _check_bool_val(dsdict[dups])
        if 'min_rows' in dsdictkeys:
            val = dsdict['min_rows']
            if not isinstance(val, int):
                raise YamlParsingError((f'dataset: min_rows want an integer, '
                                        f'got {val}({type(val)})'))
            suite.min_rows = val
    if 'columns' in ykeys:
        colslist = ymld['columns']
        if len(colslist) == 0:
            return
        for coldict in colslist:
            colkeys = list(coldict.keys())
            _checkcolumnkeys(colkeys)
            colname = coldict['name']
            coltype = coldict['type']
            _checkcolumntype(coltype)
            suite.addcolumn(colname, coltype)
