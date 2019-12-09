# DataWhistle

> We are but zookeepers taming animalistic datasets by blowing on whistles.
> -- <cite>Anonymous Data Scientist</cite>

A Python Programmatic Data Checker.

Define rules for your dataset in a yaml file (see example.yaml).  Use
DataWhistle to check if a dataset conforms to the rules.

DataWhistle currently checks two data sources. Comma Separated Value
(CSV) files are checked using [pandas](https://pandas.pydata.org),
in memory. Google BigQuery tables are checked using the
[Google Cloud SDK](https://cloud.google.com/sdk/install) command line
tools.

Example command line usage, testing a CSV file:

```sh
$ python3 -m datawhistle --csv data.csv --rules checks.yaml --verbose
Reading data file ... done.
Parsing rules file ... done.
Running checks .F....................................... done.
Checks failed (1):
want 0 duplicate rows, got 2
```
