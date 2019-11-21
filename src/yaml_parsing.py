from yaml import load  # type: ignore
from typing import Dict


def load_raw_yaml(filename: str) -> Dict:
    stream = open(filename, 'r')
    parsed = load(stream)
    return parsed


if __name__ == '__main__':
    raw: Dict = load_raw_yaml('../tests/yamls/file1.yaml')
    print(raw)
