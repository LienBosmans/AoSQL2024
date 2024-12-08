import duckdb

## Connect to DuckDB database
con = duckdb.connect("quack.db")

## Set-up DuckDB database using the SQL dump provided
# file_path = 'example.txt' # One-time setup of the example data. You can delete `quack.db` if you want to run it again.
file_path = 'setup.txt' # Setup of the actual data. It overwrites the example data.
with open(file_path, 'r') as file:
    sql_dump = file.read()

con.sql(sql_dump)

##  Write a SQL query and save as solution.csv
con.sql(
'''--sql
with prod_lag as (
    select 
        production_date,
        toys_produced,
        lag(toys_produced) over (order by production_date) as prev_day_production
    from 
        toy_production
),
prod_change as (
    select 
        production_date,
        toys_produced,
        prev_day_production,
        toys_produced - prev_day_production as prod_change,
        round( (100*(toys_produced - prev_day_production)/prev_day_production), 2) as prod_change_perc
    from 
        prod_lag
)

select * from prod_change order by prod_change_perc desc limit 1
'''
).show() #to_csv('solution.csv') # use .show() instead for a quick peak
