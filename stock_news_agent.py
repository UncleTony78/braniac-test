import os
import time
import json
import requests
import google.generativeai as genai
from dotenv import load_dotenv
from textblob import TextBlob
import streamlit as st

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

def analyze_news_with_gemini(alpha_news, fmp_news):
    """Use Gemini to analyze and summarize stock news"""
    combined_articles = []

    if alpha_news and isinstance(alpha_news, dict):
        for article in alpha_news.get("feed", []):
            if isinstance(article, dict):
                title = article.get("title", "No Title")
                summary = article.get("summary", "No summary available")
                combined_articles.append(f"Alpha Vantage: {title} - {summary}")

    if fmp_news and isinstance(fmp_news, list):
        for article in fmp_news:
            if isinstance(article, dict):
                title = article.get("title", "No Title")
                summary = article.get("summary", "No summary available")
                combined_articles.append(f"FMP: {title} - {summary}")

    # Initialize results
    results = {
        "sentiment_analysis": [],
        "summaries": []
    }

    # Stage 1: Sentiment Analysis
    for article in combined_articles:
        time.sleep(1)  # Simulate processing time
        analysis = TextBlob(article)
        sentiment = analysis.sentiment.polarity
        results["sentiment_analysis"].append({
            "article": article,
            "sentiment": sentiment
        })

    # Stage 2: Summarization
    for article in combined_articles:
        time.sleep(1)  # Simulate processing time
        summary = article[:50] + "..."  # Placeholder for actual summarization
        results["summaries"].append({
            "article": article,
            "summary": summary
        })

    return results

def main():
    st.title("Stock News Agent")
    
    st.header("Fetching News...")
    alpha_news = fetch_alpha_vantage_news()
    fmp_news = fetch_fmp_news()

    st.header("Analyzing News...")
    analysis = analyze_news_with_gemini(alpha_news, fmp_news)

    # Display AI Analysis
    st.header("AI Analysis and Suggestions")
    
    st.subheader("Sentiment Analysis:")
    for item in analysis["sentiment_analysis"]:
        st.write(f"{item['article']} - Sentiment: {item['sentiment']}")

    st.subheader("Summaries:")
    for item in analysis["summaries"]:
        st.write(f"{item['article']} - Summary: {item['summary']}")

    st.subheader("DYOR (Do Your Own Research)")
    st.write("Always verify the information and conduct your own analysis before making investment decisions.")

if __name__ == "__main__":
    main()