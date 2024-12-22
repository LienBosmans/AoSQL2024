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
with last_scores as (
    select 
        name,
        salary,
        list_last(year_end_performance_scores) as last_score
    from 
        employees
),
avg_scores as (
    select 
        avg(last_score) as avg_score
    from last_scores
),
salaries as (
    select 
        last_scores.name,
        last_scores.salary as base_salary,
        case
            when last_scores.last_score > avg_scores.avg_score
                then 0.15*last_scores.salary
            else 
                0
        end as bonus
    from
        last_scores
        left join avg_scores on 1=1
),
total_salaries as (
    select 
        name,
        base_salary + bonus as total_salary
    from 
        salaries
)
select sum(total_salary) from total_salaries
'''
).to_csv('solution.csv') # use .show() instead for a quick peak
