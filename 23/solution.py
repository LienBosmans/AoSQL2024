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
with prev_id as (
    select 
        id,
        lag(id,1,null) over (order by id) as prev_id,
        case
            when id = lag(id,1,null) over (order by id) + 1
                then 0 -- same group
            else 1 -- new group
        end as is_new_group
    from 
        sequence_table
),
groupings as (
    select 
        id,
        sum(is_new_group) over (order by id) as group_id,
    from prev_id
),
groups as (
    select 
        group_id,
        min(id) as first_id,
        max(id) as last_id
    from 
        groupings
    group by 
        group_id
),
gaps as (
    select 
        group_id,
        last_id + 1 as gap_start,
        (lead(first_id,1,null) over (order by group_id)) as gap_end
    from 
        groups
),
missing_numbers as (
    select 
        group_id,
        gap_start,
        gap_end - 1 as gap_end,
        range(gap_start,gap_end) as missing_numbers
    from 
        gaps
    where
        gap_end is not null
)


select * from missing_numbers order by group_id
'''
).to_csv('solution.csv') # use .show() instead for a quick peak
