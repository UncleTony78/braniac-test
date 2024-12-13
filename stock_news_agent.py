import os
import time
import json
import schedule
import requests
import google.generativeai as genai
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# API Keys
ALPHA_VANTAGE_KEY = "K89OKLH1HTR1ISG6"
FINHUB_KEY = "ctbh9o9r01qvslquhp6gctbh9o9r01qvslquhp70"
FMP_KEY = "78vbq4FqQlTjaAidauLyvOa0TeLoOTi9"

# Configure Gemini AI
genai.configure(api_key=os.getenv('GOOGLE_API_KEY'))
model = genai.GenerativeModel('gemini-2.0-flash-exp')

def fetch_alpha_vantage_news():
    """Fetch news from Alpha Vantage"""
    url = "https://www.alphavantage.co/query"
    params = {
        "function": "NEWS_SENTIMENT",
        "topics": "financial_markets",
        "apikey": ALPHA_VANTAGE_KEY
    }
    
    try:
        response = requests.get(url, params=params)
        return response.json()
    except Exception as e:
        print(f"Error fetching Alpha Vantage news: {e}")
        return None

def fetch_fmp_news():
    """Fetch news from Financial Modeling Prep"""
    url = f"https://financialmodelingprep.com/api/v3/stock_news?limit=50&apikey={FMP_KEY}"
    try:
        response = requests.get(url)
        return response.json()
    except Exception as e:
        print(f"Error fetching FMP news: {e}")
        return None

def fetch_market_sentiment():
    """Fetch market sentiment from Finnhub"""
    url = f"https://finnhub.io/api/v1/news-sentiment?token={FINHUB_KEY}"
    try:
        response = requests.get(url)
        return response.json()
    except Exception as e:
        print(f"Error fetching Finnhub sentiment: {e}")
        return None

def analyze_news_with_gemini(news_data):
    """Use Gemini to analyze and summarize stock news"""
    if not news_data:
        return "Unable to fetch news data."
    
    prompt = f"""
    Analyze the following financial market data and provide:
    1. Key Market Summary:
       - Major market movements
       - Notable stock performances
       - Important sector trends
    
    2. News Analysis:
       - Most significant market-moving news
       - Potential market catalysts
       - Key company developments
    
    3. Market Sentiment and Outlook:
       - Overall market sentiment
       - Short-term market outlook
       - Potential risks and opportunities

    Please provide concise, actionable insights.
    
    News data: {json.dumps(news_data, indent=2)}
    """
    
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Error analyzing news with Gemini: {e}"

def run_news_update():
    """Main function to run the news update"""
    print("\n=== Running Stock News Update ===")
    print(f"Time: {time.strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Fetch data from multiple sources
    print("Fetching news and market data...")
    news_data = {
        "alpha_vantage": fetch_alpha_vantage_news(),
        "fmp_news": fetch_fmp_news(),
        "market_sentiment": fetch_market_sentiment()
    }
    
    print("Analyzing with Gemini...")
    analysis = analyze_news_with_gemini(news_data)
    
    print("\nGemini Market Analysis:")
    print("=" * 50)
    print(analysis)
    print("=" * 50)

def main():
    print("Advanced Stock News Agent Started!")
    print("Schedule: Running daily updates at 9:00 AM")
    
    # Schedule the job to run daily at 9:00 AM
    schedule.every().day.at("09:00").do(run_news_update)
    
    # Run once immediately on startup
    run_news_update()
    
    # Keep the script running
    while True:
        schedule.run_pending()
        time.sleep(60)

if __name__ == "__main__":
    main() 