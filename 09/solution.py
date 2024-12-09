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
with avg_speed_exercise as (
    select 
        reindeer_id,
        exercise_name,
        avg(speed_record) as avg_speed
    from 
        training_sessions
    group by 
        reindeer_id,
        exercise_name
),
max_avg_speed as (
    select 
        reindeer_id,
        max(avg_speed) as top_speed
    from 
        avg_speed_exercise
    group by 
        reindeer_id
),
top_scores as (
    select 
        reindeers.reindeer_name,
        round(max_avg_speed.top_speed,2) as top_speed
    from 
        max_avg_speed
        left join reindeers
            on max_avg_speed.reindeer_id = reindeers.reindeer_id
)

select * 
from top_scores
where reindeer_name <> 'Rudolph'
order by top_speed desc
limit 3
'''
).to_csv('solution.csv') # use .show() instead for a quick peak
