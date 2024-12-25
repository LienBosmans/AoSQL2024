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
with songs_played as (
    select 
        user_plays.song_id as song_id,
        user_plays.duration as play_duration,
        songs.song_duration as song_duration,
        songs.song_title as song_title,
        case
            when play_duration = song_duration
                then 1
            else 0
        end as full_play,
        case 
            when play_duration < song_duration
                then 1
            else 0
        end as skipped,
    from
        user_plays
        left join songs
            on user_plays.song_id = songs.song_id
),
song_stats as (
    select 
        song_id,
        song_title,
        sum(full_play) as full_plays,
        sum(skipped) as skipps
    from 
        songs_played
    group by all
)

select * from song_stats order by full_plays desc, skipps asc limit 1;
'''
).to_csv('solution.csv') # use .show() instead for a quick peak
