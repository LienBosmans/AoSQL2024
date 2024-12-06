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
