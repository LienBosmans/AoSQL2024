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
with gifts_ranked as (
    select 
        gifts.gift_id,
        gifts.gift_name,
        count(*) as abs_popularity
    from 
        gift_requests
        left join gifts
            on gift_requests.gift_id = gifts.gift_id
    group by 
        gifts.gift_id,
        gifts.gift_name
),
gifts_quantiled as (
    select 
        gift_name,
        round(percent_rank() over (order by abs_popularity asc),2) as overall_rank
    from 
        gifts_ranked
),
max_rank as (
select max(overall_rank) as max_rank from gifts_quantiled
)

select * 
from gifts_quantiled
where overall_rank < (select max_rank from max_rank)
order by overall_rank desc, gift_name asc
limit 1
'''
).to_csv('solution.csv') # use .show() instead for a quick peak
