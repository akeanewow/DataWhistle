from yaml import load  # type: ignore
import pandas as pd  # type: ignore
from typing import Dict
import checksuites as cs


_YAML_TOPLEVEL_KEYS = ['dataset', 'columns']


def load_raw_yaml(filename: str) -> Dict:
    '''Parse a yaml file into a Dict object.'''
    stream = open(filename, 'r')
    parsed = load(stream)
    return parsed


def apply_yamldict_to_checksuite(ymld: Dict,
                                 suite: cs.PandasDatsetCheckSuite,
                                 df: pd.DataFrame) -> None:
    '''Apply yaml parsed into dictionary to a checksuite object.'''
    ykeys = ymld.keys()
    for key in ykeys:
        if key not in _YAML_TOPLEVEL_KEYS:
            raise AttributeError(f'Unexpected yaml attribute {key}')
    if 'dataset' in ykeys:
        dsdict = ymld['dataset']
        dsdictkeys = dsdict.keys()
        if 'stop_on_fail' in dsdictkeys:
            if dsdict['fail'] is True:
                suite.stop_on_fail = True
        if 'allow_duplicate_rows' in dsdictkeys:
            if dsdict['allow_duplicate_rows'] is False:
                suite.allow_duplicate_rows = False


if __name__ == '__main__':
    raw = load_raw_yaml('../tests/yamls/file1.yaml')
    print(raw)
