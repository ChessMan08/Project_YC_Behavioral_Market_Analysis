import pandas as pd
from pytrends.request import TrendReq
import time
import sys

# Configuration
TICKERS = [
    'AAPL', 'GOOGL', 'MSFT', 'AMZN', 'NVDA', 'TSLA', 'META',
    'NFLX', 'AMD', 'INTC', 'CRM', 'ADBE', 'PYPL', 'QCOM', 'CSCO'
]

KEYWORDS = TICKERS
TIMEFRAME = 'today 5-y'

# Data Fetching
pytrends = TrendReq(hl='en-US', tz=360)

print("Fetching weekly Google Trends data...")

# Create an empty DataFrame to store all trends data.
all_trends_data = pd.DataFrame()

# Loop through each keyword to fetch its trend data individually.
for keyword in KEYWORDS:
    print(f"Fetching data for keyword: '{keyword}'")
    try:
        pytrends.build_payload([keyword], cat=7, timeframe=TIMEFRAME, geo='', gprop='')
        interest_over_time_df = pytrends.interest_over_time()

        if not interest_over_time_df.empty:
            interest_over_time_df.rename(columns={keyword: 'score'}, inplace=True)
            # Ticker is now the same as the keyword.
            interest_over_time_df['ticker'] = keyword
            
            all_trends_data = pd.concat([all_trends_data, interest_over_time_df[['score', 'ticker']]])
        else:
            print(f"No data found for keyword: {keyword}")

        time.sleep(1)

    except Exception as e:
        print(f"An error occurred for keyword '{keyword}': {e}")

if all_trends_data.empty:
    print("\n No data was successfully fetched from Google Trends. Exiting.")
    empty_df = pd.DataFrame(columns=['date', 'ticker', 'keyword', 'score'])
    empty_df.to_csv('google_trends_data.csv', index=False)
    sys.exit()

print("Data fetched successfully. Processing...")

# Data Processing
all_trends_data.reset_index(inplace=True)
all_trends_data['date'] = pd.to_datetime(all_trends_data['date'])
all_trends_data['keyword'] = all_trends_data['ticker'] + ' stock'
final_trends_data = all_trends_data[['date', 'ticker', 'keyword', 'score']]

# Save to CSV
output_path = 'google_trends_data.csv'
final_trends_data.to_csv(output_path, index=False)

print(f"✅ Google Trends data saved successfully to {output_path}")
print(f"Shape of the data: {final_trends_data.shape}")
print("Sample of the data:")
print(final_trends_data.head())
