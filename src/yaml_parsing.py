from yaml import load  # type: ignore
from typing import Dict
import pandas as pd  # type: ignore
import checksuites as cs


def load_raw_yaml(filename: str) -> Dict:
    '''Parse a yaml file into a Dict object.'''
    stream = open(filename, 'r')
    parsed = load(stream)
    return parsed


def yamldict_to_pandaschecksuite(
        ymld: Dict,
        df: pd.DataFrame) -> cs.PandasDatsetCheckSuite:
    pdc: cs.PandasDatsetCheckSuite = cs.PandasDatsetCheckSuite(df)
    '''Convert yaml parsed into a Dict to a pandas check suite.'''
    ymldkeys = ymld.keys()
    if 'dataset' in ymldkeys:
        dsdict = ymld['dataset']
        dsdictkeys = dsdict.keys()
        if 'fail' in dsdictkeys:
            if dsdict['fail'] == True:
                pdc.fail = True
        if 'allow_duplicate_rows' in dsdictkeys:
            if dsdict['allow_duplicate_rows'] == False:
                pdc.allow_duplicate_rows = False
        if 'min_rows' in dsdictkeys:
            pass
    return pdc


if __name__ == '__main__':
    raw = load_raw_yaml('../tests/yamls/file1.yaml')
    print(raw)
