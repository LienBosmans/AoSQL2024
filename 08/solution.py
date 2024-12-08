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
recursive_management_path = con.sql(
'''--sql
with recursive calculate_path(staff_id,staff_name,next_manager_id,manager_path,manager_level) as (
    -- anchor
    select 
        staff_id,
        staff_name,
        manager_id as next_manager_id,
        staff_id::varchar as manager_path,
        1 as manager_level
    from 
        staff
    UNION ALL
    -- recursion 
    select 
        calculate_path.staff_id,
        calculate_path.staff_name,
        next_manager.manager_id as next_manager_id,
        concat(calculate_path.next_manager_id::varchar,',',calculate_path.manager_path) as manager_path,
        calculate_path.manager_level + 1 as manager_level
    from 
        calculate_path
        left join staff as next_manager 
            on calculate_path.next_manager_id = next_manager.staff_id
    where 
        -- keep going if
        calculate_path.next_manager_id is not null
)

select * from calculate_path
'''
)

con.sql(
'''--sql
with final_paths as (
    select 
        staff_id,
        staff_name,
        max(manager_level) as level,
        argmax(manager_path,manager_level) as path
    from 
        recursive_management_path
    group by 
        staff_id,
        staff_name
)

select * from final_paths order by level desc limit 1

'''
).to_csv('solution.csv') # use .show() instead for a quick peak
