# Advent of SQL 2024

https://adventofsql.com/

## Building and running a Docker container for DuckDB
Build Docker container for DuckDB:

```
docker build --progress plain -t duckdb .
```

Run Docker container for DuckDB:

```
docker run --rm -it -v path-to-your-folder:/duckdb duckdb
```

Close Docker container:
```
exit
```

## Boiler plate explained

The folder `00` contains the boiler plate to start a SQL advent day.
It contains the files:
- `example.txt`: copy the 'Table Schemas' and 'Example Data' code here
- `setup.txt`: copy whatevers in the `advent_of_sql_day_xx.sql` file you downloaded here
- `solution.py`: write your solution here
- `.gitignore`: So you don't accidently commit the final solution. Input files and the DuckDB file are also ignored.

## Syntax highlighting for SQL in Python files

There exist multiple linters and extensions for this. I'm using this one in VSCode: https://marketplace.visualstudio.com/items?itemName=chdsbd.python-inline-sql-syntax.

## Looking inside your DuckDB database `quack.db`

You can use the instructions on the DuckDB website to download and install DBeaver, a free Universal Database Manger.\
https://duckdb.org/docs/guides/sql_editors/dbeaver.html

Note that DuckDB allows only one connection at the same. If you get below error when trying to run your script, you need to first disconnect the database in DBeaver.
```
duckdb.duckdb.IOException: IO Error: Cannot open file "/duckdb/xx/quack.db": Permission denied
```

## Resolving Postgres-DuckDB incompatibilities

Since the challenges are based on Postgres, sometimes small adjustments to the input files are needed to make them compatible with DuckDB. List below
- replace `SERIAL PRIMARY KEY` by `INTEGER PRIMARY KEY` and mimic the auto incrementing key functionality where needed (only needed for the examples):
    - create a custom key-generator such as `CREATE SEQUENCE seq_child_id START 1;`
    - add that as an extra argument to the `INSERT INTO` statement:
        ```
        INSERT INTO children (child_id, name, age, city) VALUES
            (nextval('seq_child_id'),'Tommy', 8, 'London'),
            ...
        ```
- The error `Constraint Error: Violates foreign key constraint because key "..." does not exist in the referenced table` can be resolved by simply deleting the statement `FOREIGN KEY (...) REFERENCES Table(table_id)` from the input file.

Because DuckDB doesn't support data type XML, I skipped the challenge of day 3 for now.
