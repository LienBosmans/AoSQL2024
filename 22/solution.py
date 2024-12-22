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
with skill_lists as (
    select
        elf_name,
        string_split(skills,',') as skill_list
    from 
        elves
),
sql_elves as (
    select 
        elf_name,
        skill_list
    from 
        skill_lists
    where 
        list_contains(skill_list,'SQL')
    order by 
        elf_name
)

select count(*) from sql_elves
'''
).to_csv('solution.csv') # use .show() instead for a quick peak
