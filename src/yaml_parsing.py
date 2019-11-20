from yaml import load
try:
    from yaml import CLoader as Loader
except ImportError:
    from yaml import Loader


def load_rules_from_yaml(filename: str):
    stream = open(filename, 'r')
    parsed = load(stream)
    print(parsed)


if __name__ == '__main__':
    load_rules_from_yaml('../tests/yamls/file1.yaml')
