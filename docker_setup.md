Build Docker container for DuckDB:

```
docker build --progress plain -t duckdb .
```

Run Docker containeer for DuckDB:

```
docker run --rm -it -v C:\github_projects\AoSQL2024\:/duckdb duckdb
```