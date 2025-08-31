with source as (

    select *
    from read_csv_auto('../google_trends_data.csv')

),

renamed as (

    select
        cast("date" as date) as metric_date,
        cast("ticker" as varchar) as ticker,
        cast("score" as integer) as trend_score
    from
        source

)

select * from renamed