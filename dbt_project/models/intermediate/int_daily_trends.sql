with trends_data as (
    select * from {{ ref('stg_trends_data') }}
),

date_range as (
    select
        min(metric_date) as start_date,
        max(metric_date) as end_date
    from {{ ref('stg_trends_data') }}
),

all_dates as (
    select
        cast(range as date) as metric_date
    from
        range(
            (select start_date from date_range),
            (select end_date + interval '1 day' from date_range),
            interval '1 day'
        )
),

daily_trends as (
    select
        d.metric_date,
        tickers.ticker,
        last_value(td.trend_score ignore nulls) over (
            partition by tickers.ticker 
            order by d.metric_date
            rows between unbounded preceding and current row
        ) as trend_score
    from 
        all_dates d
    cross join (select distinct ticker from trends_data) as tickers
    left join trends_data td 
        on d.metric_date = td.metric_date and tickers.ticker = td.ticker
)

select * from daily_trends