# DataWhistle

> We are but zookeepers taming animalistic datasets by blowing on whistles.
> -- <cite>Anonymous Data Scientist</cite>

A Python Programmatic Data Checker.

Define rules for your dataset in a yaml file (see example.yaml).  Use whistle.py to check if a dataset conforms to the rules.

Example command line usage:

```sh
$ python3 -m datawhistle --csv data.csv --rules checks.yaml --verbose
Reading data file ... done.
Parsing rules file ... done.
Running checks .F....................................... done.
Checks failed (1):
want 0 duplicate rows, got 2
```

### Status

DataWhistle is in active development and the API is not yet stable.
