with source as (

    select *
    from read_csv_auto('../market_data.csv')

),

renamed as (

    select
        cast("date" as date) as metric_date,
        cast("ticker" as varchar) as ticker,
        cast("open" as double) as open_price,
        cast("high" as double) as high_price,
        cast("low" as double) as low_price,
        cast("close" as double) as close_price,
        cast("volume" as bigint) as trading_volume
    from
        source

)

select * from renamed