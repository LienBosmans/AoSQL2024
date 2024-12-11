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
with pivot_data as (
    pivot drinks
    on drink_name
    using sum(quantity)
    group by date
)

select * 
from pivot_data
where
    "Eggnog" = 198 --50
    and "Hot Cocoa" = 38 --75
    and "Peppermint Schnapps" = 298 --30
'''
).to_csv('solution.csv') # use .show() instead for a quick peak
