import duckdb

## Connect to DuckDB database
con = duckdb.connect("quack.db")

# Use spatial extension
con.sql(
'''--sql
install spatial;
load spatial;
'''
)

## Set-up DuckDB database using the SQL dump provided
# file_path = 'example.txt' # One-time setup of the example data. You can delete `quack.db` if you want to run it again.
file_path = 'setup.txt' # Setup of the actual data. It overwrites the example data.
with open(file_path, 'r') as file:
    sql_dump = file.read()

con.sql(sql_dump)

##  Write a SQL query and save as solution.csv
con.sql(
'''--sql
with time_windows as (
    select 
        timestamp as from_time,
        lead(timestamp,1) over (order by timestamp) as until_time,
        coordinate
    from
        sleigh_locations
),
time_spent as (
    select 
        time_windows.until_time - time_windows.from_time as duration,
        areas.place_name as location
    from 
        time_windows
        left join areas
            on ST_within(time_windows.coordinate, areas.polygon)
),
total_time_spent as (
    select 
        location,
        sum(extract(epoch from duration)) as duration
    from 
        time_spent
    group by 
        location
)

select * from total_time_spent order by duration desc limit 1
'''
).to_csv('solution.csv') # use .show() instead for a quick peak
