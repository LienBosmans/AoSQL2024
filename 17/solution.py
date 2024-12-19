import duckdb

## Connect to DuckDB database
con = duckdb.connect("quack.db")

# Use icu extension
con.sql(
'''--sql
install icu;
load icu;
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
with timezoned_workshops as (
    select 
        workshop_id,
        workshop_name,
        timezone(timezone, today() + business_start_time) as start_time,
        timezone(timezone, today() + business_end_time) as end_time
    from 
        workshops
),
earliest as (
    select 
        max(start_time)
    from 
        timezoned_workshops
    where 
        start_time >= today() + make_time(9,0,0)
)

select * from earliest
'''
).to_csv('solution.csv') # use .show() instead for a quick peak
