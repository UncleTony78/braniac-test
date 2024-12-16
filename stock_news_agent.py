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
ALPHA_VANTAGE_KEY = os.getenv("ALPHA_VANTAGE_KEY")
FINHUB_KEY = os.getenv("FINHUB_KEY")
FMP_KEY = os.getenv("FMP_KEY")

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

    # Prepare prompt for AI analysis
    prompt = f"Analyze the all of these and provide financial insights, ensure that the analysis is accurate and the data is fact checked. Ensure that you do a deep dive into the data and provide a detailed analysis:\n\n" + "\n".join(combined_articles)

    try:
        response = model.generate_content(prompt)
        analysis_result = response.text
        return analysis_result
    except Exception as e:
        return f"Error analyzing news with Gemini: {e}"

def main():
    st.title("Stock News Agent")
    
    # Create tabs for analysis and chat
    tab1, tab2 = st.tabs(["Analysis", "Chat"])

    with tab1:
        st.header("Fetching News...")
        alpha_news = fetch_alpha_vantage_news()
        fmp_news = fetch_fmp_news()

        st.header("Analyzing News...")
        analysis = analyze_news_with_gemini(alpha_news, fmp_news)

        # Display AI Analysis
        st.header("AI Analysis and Suggestions")
        st.write(analysis)

    with tab2:
        st.subheader("Chat with AI")
        if 'messages' not in st.session_state:
            st.session_state.messages = []

        user_input = st.text_input("You: ", "")
        
        if st.button("Send"):
            if user_input:
                st.session_state.messages.append({"role": "user", "content": user_input})
                
                # Prepare the context for AI response
                context = "\n".join([f"{msg['role']}: {msg['content']}" for msg in st.session_state.messages])
                prompt = f"Based on the previous analysis and the following conversation, respond to the user:\n\n{context}"

                # Get AI response
                response = model.generate_content(prompt)
                ai_response = response.text
                
                # Add AI response to messages
                st.session_state.messages.append({"role": "assistant", "content": ai_response})

        # Display chat messages
        for message in st.session_state.messages:
            if message["role"] == "user":
                st.write(f"You: {message['content']}")
            else:
                st.write(f"AI: {message['content']}")

if __name__ == "__main__":
    main()