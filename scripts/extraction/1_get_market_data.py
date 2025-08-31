import yfinance as yf
import pandas as pd
from datetime import date, timedelta

TICKERS = [
    'AAPL', 'GOOGL', 'MSFT', 'AMZN', 'NVDA', 'TSLA', 'META',
    'NFLX', 'AMD', 'INTC', 'CRM', 'ADBE', 'PYPL', 'QCOM', 'CSCO'
]

# Set the time period for data collection.
END_DATE = date.today()
START_DATE = END_DATE - timedelta(days=10*365)

print("Fetching daily market data...")

# Download historical data for all tickers.
market_data_multi = yf.download(
    tickers=TICKERS,
    start=START_DATE,
    end=END_DATE,
    group_by='ticker'
)

print("Data fetched successfully. Processing...")

# Data Processing
market_data = market_data_multi.stack(level=0).reset_index()
market_data.rename(columns={'level_1': 'Ticker'}, inplace=True)
market_data.columns = market_data.columns.str.lower()

market_data['date'] = pd.to_datetime(market_data['date'])

# Save to CSV 
output_path = 'market_data.csv'
market_data.to_csv(output_path, index=False)

print(f"✅ Market data saved successfully to {output_path}")
print(f"Shape of the data: {market_data.shape}")
print("Sample of the data:")
print(market_data.head())
