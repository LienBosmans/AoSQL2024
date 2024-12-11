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
with add_season_num as (
    select 
        field_name,
        harvest_year,
        case
            when season = 'Spring' then 1
            when Season = 'Summer' then 2
            when season = 'Fall' then 3
            when season = 'Winter' then 4
            else -1
        end as quarter,
        season,
        trees_harvested
    from 
        treeharvests
),
add_last_2_seasons as (
    select 
        field_name,
        harvest_year,
        quarter,
        season,
        trees_harvested as this_harvest,
        lag(trees_harvested,1,null) over (partition by field_name order by harvest_year,quarter) as prev_harvest,
        lag(trees_harvested,2,null) over (partition by field_name order by harvest_year,quarter) as prev_prev_harvest
    from
        add_season_num
),
moving_average as (
    select 
        field_name,
        harvest_year,
        quarter,
        season,
        coalesce(
            round((this_harvest + prev_harvest + prev_prev_harvest)/3,2),
            round((this_harvest + prev_harvest)/2,2),
            round(this_harvest)
        ) as moving_average 
    from 
        add_last_2_seasons
)

select * from moving_average order by moving_average desc limit 1
'''
).to_csv('solution.csv') # use .show() instead for a quick peak
