import duckdb

## Connect to DuckDB database
con = duckdb.connect("quack.db")

## Set-up DuckDB database using the SQL dump provided
# file_path = 'example.txt' # One-time setup of the example data. You can delete `quack.db` if you want to run it again.
file_path = 'setup.txt' # Setup of the actual data. It overwrites the example data.
with open(file_path, 'r') as file:
    sql_dump = file.read()

con.sql(sql_dump)

#  Write a SQL query and save as solution.csv
con.sql(
'''--sql
with elf_ranking as (
    select 
        elf_id,
        elf_name,
        primary_skill,
        years_experience,
        row_number() over (partition by primary_skill order by years_experience, elf_id) as worst_ranking,
        row_number() over (partition by primary_skill order by years_experience desc, elf_id) as best_ranking
    from 
        workshop_elves
),
elf_pairing as (
    select
        best_elf.elf_id as max_years_experience_elf_id,
        -- best_elf.elf_name as best,
        worst_elf.elf_id as max_years_experience_elf_id,
        -- worst_elf.elf_name as worst,
        best_elf.primary_skill as shared_skill
    from 
        elf_ranking as best_elf
        inner join elf_ranking as worst_elf
            on (
                best_elf.primary_skill = worst_elf.primary_skill
                and best_elf.best_ranking = 1
                and worst_elf.worst_ranking = 1
            )
)

select * from elf_pairing order by shared_skill
'''
).to_csv('solution.csv') # use .show() instead for a quick peak
