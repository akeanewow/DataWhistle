from yaml import load  # type: ignore
from typing import Dict, List
import checksuites as cs


_YAML_TOPLEVEL_KEYS = ['dataset', 'columns']
_YAML_DATASET_KEYS = ['stop_on_fail', 'allow_duplicate_rows', 'min_rows']


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


if __name__ == '__main__':
    raw = load_raw_yaml('../tests/yamls/file1.yaml')
    print(raw)
