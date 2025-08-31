import pandas as pd
from newsapi import NewsApiClient
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from datetime import date, timedelta

# Configuration
NEWS_API_KEY = 'e0b17a061801424ebd382809fc37c665' 

# Map tickers to a more search-friendly company name.
COMPANY_NAMES = {
    'AAPL': 'Apple', 'GOOGL': 'Google', 'MSFT': 'Microsoft', 'AMZN': 'Amazon',
    'NVDA': 'NVIDIA', 'TSLA': 'Tesla', 'META': 'Meta', 'NFLX': 'Netflix',
    'AMD': 'AMD', 'INTC': 'Intel', 'CRM': 'Salesforce', 'ADBE': 'Adobe',
    'PYPL': 'PayPal', 'QCOM': 'Qualcomm', 'CSCO': 'Cisco'
}
# Define the date range for news articles
END_DATE = date.today()
START_DATE = END_DATE - timedelta(days=29)

# Initialization
newsapi = NewsApiClient(api_key=NEWS_API_KEY)
# Initialize the VADER sentiment analyzer.
analyzer = SentimentIntensityAnalyzer()

print("Fetching news articles and calculating sentiment...")

# Data Fetching and Sentiment Analysis
all_articles_data = []

# Loop through each company to fetch news and analyze sentiment.
for ticker, company_name in COMPANY_NAMES.items():
    print(f"Fetching news for {company_name} ({ticker})...")
    try:
        # Fetch articles from NewsAPI.
        all_articles = newsapi.get_everything(
            q=company_name,
            from_param=START_DATE.strftime('%Y-%m-%d'),
            to=END_DATE.strftime('%Y-%m-%d'),
            language='en',
            sort_by='relevancy',
            page_size=100
        )
        
        # Process each article.
        for article in all_articles['articles']:
            # Combine title and description for a richer sentiment analysis.
            text_to_analyze = f"{article['title']}. {article['description']}"
            
            # Get sentiment scores using VADER.
            sentiment_scores = analyzer.polarity_scores(text_to_analyze)
            
            # We are most interested in the 'compound' score, which is a normalized, weighted composite score.
            compound_score = sentiment_scores['compound']
            
            # Append the structured data to our list.
            all_articles_data.append({
                'ticker': ticker,
                'date': pd.to_datetime(article['publishedAt']).date(), # Just the date part
                'headline': article['title'],
                'sentiment_score': compound_score
            })
            
    except Exception as e:
        print(f"An error occurred for {company_name}: {e}")

print("Data fetched successfully. Creating DataFrame...")

# Create DataFrame and Save
# Convert the list of dictionaries into a Pandas DataFrame.
news_sentiment_df = pd.DataFrame(all_articles_data)
# Ensure date column is in datetime format.
news_sentiment_df['date'] = pd.to_datetime(news_sentiment_df['date'])

# Save the DataFrame to a CSV file.
output_path = 'news_sentiment_data.csv'
news_sentiment_df.to_csv(output_path, index=False)

print(f"✅ News sentiment data saved successfully to {output_path}")
print(f"Shape of the data: {news_sentiment_df.shape}")
print("Sample of the data:")
print(news_sentiment_df.head())