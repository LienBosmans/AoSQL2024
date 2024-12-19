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
staff_levels = con.sql(
'''--sql
with recursive staff_levels as (
    select 
        staff_id,
        staff_name,
        1 as level,
        null as manager_id,
        staff_id::varchar as path
    from 
        staff
    where 
        manager_id is null
    union all 
    select 
        staff.staff_id as staff_id,
        staff.staff_name as staff_name,
        staff_levels.level + 1 as level,
        staff.manager_id as manager_id,
        concat(staff_levels.path,',',staff.staff_id::varchar)
    from 
        staff
        inner join staff_levels
            on staff.manager_id = staff_levels.staff_id
)

select * from staff_levels
'''
)

# correct answer (using peers = elves at the same level reporting to the same manager)
con.sql(
'''--sql
with staff_peers as (
    select 
        staff.staff_id,
        staff.staff_name,
        staff.level,
        count(peers.staff_id) as count_peers
    from 
        staff_levels as staff
        left join staff_levels as peers 
            on (
                staff.level = peers.level
                and staff.manager_id = peers.manager_id
            )
    group by all
)

select * from staff_peers order by count_peers desc, level desc, staff_id asc limit 1
'''
).show() 

# accepted answer: (using peers = elves at the same level)
con.sql('''--sql
with peers_by_level as (
    select 
        level,
        count(staff_id) as peer_count
    from
        staff_levels
    group by
        level
    order by 
        count(staff_id) desc
),
most_peers as (
    select 
        staff_id,
        level
    from 
        staff_levels
    where 
        level = (select arg_max(level,peer_count) from peers_by_level)
)
        
select * from most_peers order by level desc, staff_id asc limit 1
'''
).to_csv('solution.csv') # use .show() instead for a quick peak
