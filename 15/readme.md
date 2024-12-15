For day 15, you can use the `spatial` extension for DuckDB.
- Replace `GEOGRAPHY(POINT)` by `POINT_2D`
- Replace `GEOGRAPHY(POLYGON)` by `POLYGON_2D`
- Remove the function `ST_SetSRID(..., 4326)`. Keep the `...` ( `ST_Point()` or `ST_GeomFromText('POLYGON())`)
