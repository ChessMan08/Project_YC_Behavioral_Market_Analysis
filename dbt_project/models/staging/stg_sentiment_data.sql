with source as (

    select *
    from read_csv_auto('../news_sentiment_data.csv')

),

renamed as (
    select
        cast("date" as date) as metric_date,
        cast("ticker" as varchar) as ticker,
        cast("headline" as varchar) as headline,
        cast("sentiment_score" as double) as sentiment_score
    from
        source
)

select * from renamed