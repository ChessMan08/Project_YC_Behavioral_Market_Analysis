with daily_metrics as (
    select * from {{ ref('int_daily_market_metrics') }}
),

daily_trends as (
    select * from {{ ref('int_daily_trends') }}
),

daily_returns as (
    select
        *,
        (close_price - lag(close_price, 1) over (partition by ticker order by metric_date)) 
            / lag(close_price, 1) over (partition by ticker order by metric_date) as daily_return
    from
        daily_metrics
),

final as (
    select
        dr.metric_date,
        dr.ticker,
        dr.open_price,
        dr.high_price,
        dr.low_price,
        dr.close_price,
        dr.trading_volume,
        dr.avg_daily_sentiment_score,
        dr.num_articles_today,
        coalesce(dt.trend_score, 0) as trend_score,
        dr.daily_return,

        avg(dr.avg_daily_sentiment_score) over (
            partition by dr.ticker 
            order by dr.metric_date 
            rows between 6 preceding and current row
        ) as sentiment_7d_avg,

        avg(dr.num_articles_today) over (
            partition by dr.ticker 
            order by dr.metric_date 
            rows between 6 preceding and current row
        ) as articles_7d_avg,

        stddev_pop(dr.daily_return) over (
            partition by dr.ticker 
            order by dr.metric_date 
            rows between 6 preceding and current row
        ) as volatility_7d,

        stddev_pop(dr.daily_return) over (
            partition by dr.ticker 
            order by dr.metric_date 
            rows between 29 preceding and current row
        ) as volatility_30d

    from
        daily_returns as dr
    left join
        daily_trends as dt
        on dr.metric_date = dt.metric_date and dr.ticker = dt.ticker
)

select * from final