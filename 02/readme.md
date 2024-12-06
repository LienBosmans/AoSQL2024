Below error can be solved by replacing `SERIAL PRIMARY KEY` with `INTEGER` (twice) in the input files `example.txt` and `setup.txt`.
```
duckdb.duckdb.CatalogException: Catalog Error: Type with name SERIAL does not exist!
```
