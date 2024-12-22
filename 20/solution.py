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
with split_url as (
    select 
        url,
        list_distinct(string_split(string_split(url,'?')[2],'&')) as param_defs
    from 
        web_requests
),
parse_url as (
    select 
        url,
        param_defs
    from 
        split_url
    where 
        list_contains(param_defs,'utm_source=advent-of-sql')
),
unique_params as (
    select 
        url,
        param_defs,
        list_distinct(
                list_transform(param_defs,x -> string_split(x,'=')[1])
        ) as params
    from 
        parse_url
)

select arg_max(url,len(params) order by url) from unique_params
'''
).to_csv('solution.csv') # use .show() instead for a quick peak
