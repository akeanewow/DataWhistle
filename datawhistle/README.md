### Source code file overview

| File             | Purpose                                                           |
|------------------|-------------------------------------------------------------------|
| pandaschecks.py  | Base data checks of a Pandas DataFrame (start here to add checks) |
| bqchecks.py      | Base data checks of a BigQuery table                              |
| checksuites.py   | Classes used to process checks and plug in different data sources |
| yamlparsing.py   | Functions to parse rules file and apply it to checksuite classes  |
| commandline.py   | Command line functions                                            |

Unit testing files have equivalent names starting with 'test_'.

### checksuites.py class hierarchy

| Class                     | Purpose                                       |
|---------------------------|-----------------------------------------------|
| TableCheckSuite           | Table level check processor (common methods)  |
| - PandasDatasetCheckSuite | Pandas DataFrame level checks                 |
| - BqTableCheckSuite       | BigQuery table level checks                   |
| ColumnCheckSuite          | Column level check processor (common methods) |
| - PandasColumnCheckSuite  | Pandas column / Series level checks           |
| - BqColumnCheckSuite      | BigQuery column level checks                  |

### Steps to add a new check

1. Add a check and equivalent unit test to base data check file e.g. pandaschecks.py.
1. Update the classes in checksuites.py.
   1. `TableCheckSuite` for talbe level checks. `ColumnCheckSuite` for column level checks.
      1. Add a check property to `__init__` method.
      1. Add an abstract method to run the check to be overriden in child classes.
      1. Add logic to `_assemble_checks` method to add the check for processing.
   1. Implement an override method in the relevant child class e.g. `PandasColumnCheckSuite` for Pandas checks.
      Call on the check implemented in step 1.
   1. Unit tests will ordinarily not need to be udpated.
1. Update the YAML processing rules in yaml_parsing.py.
   1. Add new check key values to constants at the top of the file.
   1. Update `apply_yamldict_to_checksuite` logic to convert YAML and add it to the checksuite class.
1. Update test_commandline.py with any new unit tests and changes in command line output.
1. Run mypy and flake8 on all files and check that all tests pass.
