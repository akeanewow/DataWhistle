#### BigQuery testing

BigQuery unit tests assume that the files in the testing/data directory have
been uploaded to BigQuery tables with naming convention file*.csv
becoming table*, in a dataset called 'datawhistle'. The testing tables need
to be accessible through the bq commandline tool i.e. the user is already
logged into a test project with the test data pre-loaded.

bq commands to load the test files:

```sh
bq mk datawhistle  # if it doesn't already exist
bq load --source_format=CSV --autodetect datawhistle.table1 test/data/file1.csv
bq load --source_format=CSV --autodetect datawhistle.table2 test/data/file2.csv
```

### BigQuery command examples

Once test files have been loaded to tables, the following commands can be used
to examine the test data. See the
[bq cli reference](https://cloud.google.com/bigquery/docs/reference/bq-cli-reference)
for detail.

| Command                                | Purpose                  |
|----------------------------------------|--------------------------|
| `bq ls`                                | List datasets            |
| `bq ls [dataset]`                      | List tables in a dataset |
| `bq show [dataset].[table]`            | Show table metadata      |
| `bq head -n 10 [dataset].[table name]` | Print first n rows       |
| `bq query '[SQL statements]'`          | Execute an SQL query     |
