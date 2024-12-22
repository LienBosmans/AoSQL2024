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
with q_sales as (
    select 
        year(sale_date) as year,
        case 
            when month(sale_date) in (1,2,3) then 1
            when month(sale_date) in (4,5,6) then 2
            when month(sale_date) in (7,8,9) then 3
            when month(sale_date) in (10,11,12) then 4
            else 0
        end as quarter,
        sum(amount) as amount
    from 
        sales
    group by 
        year, quarter
),
lag_sales as (
    select 
        year,quarter,
        amount,
        lag(amount,1,null) over (order by year,quarter) as prev_amount
    from 
        q_sales
),
growth as (
    select 
        year,quarter,
        amount,
        (amount - prev_amount)/(prev_amount) as growth_rate
    from 
        lag_sales
)
select concat(year,',',quarter) from growth order by growth_rate desc limit 1
'''
).to_csv('solution.csv') # use .show() instead for a quick peak
