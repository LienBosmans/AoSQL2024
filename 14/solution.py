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
with unnested_records as (
    select 
        record_id,
        record_date,
        unnest(cleaning_receipts) as receipt
    from
        santarecords
),
green_suit_records as (
    select 
        record_id,
        record_date,
        json_extract_string(receipt, '$.drop_off')::varchar as drop_off
    from 
        unnested_records
    where 
        json_extract_string(receipt, '$.color')::varchar = 'green'
        and json_extract_string(receipt, '$.garment')::varchar = 'suit'
)

select * from green_suit_records order by drop_off desc limit 1

'''
).to_csv('solution.csv') # use .show() instead for a quick peak
