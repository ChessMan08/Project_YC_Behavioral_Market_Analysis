-- Import CTEs for our staging models
with market_data as (
    select * from {{ ref('stg_market_data') }}
),

sentiment_data as (
    select * from {{ ref('stg_sentiment_data') }}
),

-- Aggregate the sentiment data to get one score per ticker per day
aggregated_sentiment as (

    select 
        metric_date, 
        ticker,
        avg(sentiment_score) as avg_daily_sentiment_score,
        count(headline) as num_articles_today
    from
        sentiment_data
    group by
        metric_date, ticker

),

-- Join the aggregated sentiment to the daily market data
final as (

    select
        md.metric_date,
        md.ticker,
        md.open_price,
        md.high_price,
        md.low_price,
        md.close_price,
        md.trading_volume,
        -- Use a coalesce to fill in 0 for days with no news
        coalesce(agg_s.avg_daily_sentiment_score, 0) as avg_daily_sentiment_score,
        coalesce(agg_s.num_articles_today, 0) as num_articles_today
    from
        market_data as md
    left join
        aggregated_sentiment as agg_s
        on md.metric_date = agg_s.metric_date and md.ticker = agg_s.ticker

)

select * from final