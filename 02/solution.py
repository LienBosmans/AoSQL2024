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
with letters as (
    select * from letters_a
    UNION ALL
    select * from letters_b
),
decoded_letters as (
    select
        id,
        chr(value) as letter,
        regexp_matches(chr(value),'[a-zA-Z !''\(\),-\.:;\?]') as not_noise
    from 
        letters
)
select
    string_agg(letter,'' order by id) as letter
from
    decoded_letters
where 
    not_noise = true
'''
).to_csv('solution.csv') # use .show() instead for a quick peak
