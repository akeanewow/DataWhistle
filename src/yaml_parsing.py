from yaml import load  # type: ignore
from typing import Dict, List
import checksuites as cs


_YAML_TOPLEVEL_KEYS = ['dataset', 'columns']
_YAML_DATASET_KEYS = ['stop_on_fail', 'allow_duplicate_rows', 'min_rows']
_YAML_COLUMN_KEYS = ['name', 'type']
_YAML_COLUMN_TYPES = ['numeric', 'string']


def load_raw_yaml(filename: str) -> Dict:
    '''Parse a yaml file into a Dict object.'''
    stream = open(filename, 'r')
    parsed = load(stream)
    return parsed


def _checktoplevelkeys(ykeys: List[str]) -> None:
    for key in ykeys:
        if key not in _YAML_TOPLEVEL_KEYS:
            raise AttributeError(f'unexpected yaml attribute {key}')


def _checkdatasetkeys(dsdictkeys: List[str]) -> None:
    for key in dsdictkeys:
        if key not in _YAML_DATASET_KEYS:
            raise AttributeError(f'unexpected dataset attribute {key}')


def _checkcolumnkeys(colkeys: List[str]) -> None:
    if 'name' not in colkeys:
        raise AttributeError('column name missing')
    if 'type' not in colkeys:
        raise AttributeError('column type missing')
    for key in colkeys:
        if key not in _YAML_COLUMN_KEYS:
            raise AttributeError(f'unexpected column attribute {key}')


def _checkcolumntype(coltype: str) -> None:
    if coltype not in _YAML_COLUMN_TYPES:
        raise AttributeError(f'column type {coltype} not recognised')


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
            if dsdict['fail'] is True:
                suite.stop_on_fail = True
        if 'allow_duplicate_rows' in dsdictkeys:
            if dsdict['allow_duplicate_rows'] is False:
                suite.allow_duplicate_rows = False
        if 'min_rows' in dsdictkeys:
            val = dsdict['min_rows']
            if not isinstance(val, int):
                raise AttributeError((f'dataset: min_rows want an integer, '
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
