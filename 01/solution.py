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
with unnested_whishlist as (
    select 
        list_id,
        child_id,
        json_extract_string(wishes, '$.first_choice')::varchar as first_choice,
        json_extract_string(wishes, '$.second_choice')::varchar as second_choice,
        json_extract_string(wishes, '$.colors[*]')::varchar[] as colors,
        submitted_date
    from 
        wish_lists
),
labeled_toy_catalogue as (
    select 
        toy_id,
        toy_name,
        category,
        case 
            when category = 'outdoor' 
                then 'Outside Workshop'
            when category = 'educational'
                then 'Learning Workshop'
            else 
                'General Workshop'
        end as workshop_assignment,
        difficulty_to_make,
        case
            when difficulty_to_make = 1
                then 'Simple Gift'
            when difficulty_to_make = 2
                then 'Moderate Gift'
            when difficulty_to_make >= 3
                then 'Complex Gift'
            else 
                NULL
        end as gift_complexity
    from 
        toy_catalogue
)
select 
    c.name,
    wl.first_choice as primary_wish,
    wl.second_choice as backup_wish,
    wl.colors[1] as favorite_color,
    len(colors) as color_count,
    tc.gift_complexity as gift_complexity,
    tc.workshop_assignment as workshop_assignment
from 
    children as c
    left join unnested_whishlist as wl
        on c.child_id = wl.child_id
    left join labeled_toy_catalogue as tc
        on tc.toy_name = wl.first_choice
order by 
    c.name asc
limit 5
'''
).to_csv('solution.csv')
