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
with child_gift as (
    select 
        children.child_id,
        children.name,
        children.city,
        gifts.price
    from 
        children
        left join gifts 
            on children.child_id = gifts.child_id
),
avg_gift as (
    select 
        avg(price) as avg_price
    from 
        child_gift
),
include_avg_gift_price as (
    select 
        child_gift.child_id,
        child_gift.name,
        child_gift.city,
        child_gift.price,
        avg_gift.avg_price
    from 
        child_gift
        left join avg_gift
            on 1=1
)

select *
from include_avg_gift_price 
where price > avg_price
order by price asc
limit 1
'''
).to_csv('solution.csv') # use .show() instead for a quick peak
