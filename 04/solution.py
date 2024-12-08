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
with comparisson as (
    select
        *,
        list_filter(new_tags, x -> not(list_contains(previous_tags,x))) as added_tags,
        list_intersect(previous_tags,new_tags) as unchanged_tags,
        list_filter(previous_tags, x -> not(list_contains(new_tags,x))) as removed_tags
    from 
        toy_production
),
count_tags as (
    select 
        toy_id,
        len(added_tags) as added_tag_count,
        len(unchanged_tags) as unchanged_tag_count,
        len(removed_tags) as removed_tag_count
    from 
        comparisson
)

select * from count_tags order by added_tag_count desc limit 1
'''
).to_csv('solution.csv') # use .show() instead for a quick peak
