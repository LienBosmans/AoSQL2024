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
with emails as (
    select 
        unnest(email_addresses) as email
    from
        contact_list
),
email_domains as (
    select 
        email,
        split_part(email,'@',2) as domain
    from
        emails
),
domain_users as (
    select 
        domain,
        count(*) as total_users,
        list(email) as users 
    from 
        email_domains
    group by 
        domain
)

select * from domain_users order by total_users desc limit 1
'''
).to_csv('solution.csv') # use .show() instead for a quick peak
