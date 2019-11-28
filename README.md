# DataWhistle

> We are but zookeepers taming animalistic datasets by blowing on whistles.
> -- <cite>Anonymous Data Scientist</cite>

A Python Programmatic Data Checker.

Define rules for your dataset in a yaml file (see example.yaml).  Use
DataWhistle to check if a dataset conforms to the rules.

Example command line usage:

```sh
$ python3 -m datawhistle --csv data.csv --rules checks.yaml --verbose
Reading data file ... done.
Parsing rules file ... done.
Running checks .F....................................... done.
Checks failed (1):
want 0 duplicate rows, got 2
```

### Data sources

DataWhistle currently checks two data sources.

Comma Separated Value (CSV) files are checked using
[pandas](https://pandas.pydata.org), in memory.

Google BigQuery tables are checked using the
[Google Cloud SDK](https://cloud.google.com/sdk/install) command line
tools. When running checks it is assumed that the user has logged into a
project using the
[gcloud init](https://cloud.google.com/sdk/gcloud/reference/init) command.
The bq scripting command is used to execute checks in BigQuery.

### Status

DataWhistle is in active development and the API is not yet stable.
