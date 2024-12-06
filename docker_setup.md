Build Docker container for DuckDB:

```
docker build --progress plain -t duckdb .
```

Run Docker container for DuckDB:

```
docker run --rm -it -v C:\github_projects\AoSQL2024\:/duckdb duckdb
```

Close Docker container:
```
exit
```