import os
import requests
import google.generativeai as genai
from dotenv import load_dotenv
import streamlit as st
import yfinance as yf
import plotly.graph_objs as go

# Load environment variables
load_dotenv()

# API Keys
ALPHA_VANTAGE_KEY = os.getenv("ALPHA_VANTAGE_KEY")
FINHUB_KEY = os.getenv("FINHUB_KEY")
SEC_API_KEY = os.getenv("SEC_API_KEY")
SIMFIN_KEY = os.getenv("SIMFIN_KEY")
POLYGON_KEY = os.getenv("POLYGON_KEY")

# Configure Gemini AI
genai.configure(api_key=os.getenv('GOOGLE_API_KEY'))
model = genai.GenerativeModel('gemini-2.0-flash-exp')

# Fetch news from Alpha Vantage
def fetch_alpha_vantage_news():
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
        st.error(f"Error fetching Alpha Vantage news: {e}")
        return None

# Fetch real-time market data from Finnhub
def fetch_finnhub_data(symbol):
    url = f"https://finnhub.io/api/v1/quote"
    params = {
        "symbol": symbol,
        "token": FINHUB_KEY
    }
    try:
        response = requests.get(url, params=params)
        return response.json()
    except Exception as e:
        st.error(f"Error fetching Finnhub data: {e}")
        return None

# Fetch filings from the SEC
def fetch_sec_data(cik):
    url = f"https://www.sec.gov/cgi-bin/browse-edgar"
    params = {
        "action": "getcompany",
        "cik": cik,
        "type": "10-K",
        "output": "atom",
        "apikey": SEC_API_KEY
    }
    try:
        response = requests.get(url, params=params)
        return response.text
    except Exception as e:
        st.error(f"Error fetching SEC data: {e}")
        return None

# Fetch data from Simfin
def fetch_simfin_data(symbol):
    url = f"https://simfin.com/api/v1/companies"
    params = {
        "api-key": SIMFIN_KEY,
        "ticker": symbol
    }
    try:
        response = requests.get(url, params=params)
        return response.json()
    except Exception as e:
        st.error(f"Error fetching Simfin data: {e}")
        return None

# Fetch data from Polygon.io
def fetch_polygon_data(symbol):
    url = f"https://api.polygon.io/v1/open-close/{symbol}/2023-12-15"
    params = {
        "apiKey": POLYGON_KEY
    }
    try:
        response = requests.get(url, params=params)
        return response.json()
    except Exception as e:
        st.error(f"Error fetching Polygon data: {e}")
        return None

# Fetch stock data from Yahoo Finance
def fetch_stock_data(ticker, start_date, end_date):
    stock_data = yf.download(ticker, start=start_date, end=end_date)
    return stock_data

# Analyze the stock chart and generate insights
def analyze_chart(stock_data):
    fig = go.Figure()

    # Add a trace for the closing prices
    fig.add_trace(go.Scatter(x=stock_data.index, y=stock_data['Close'], mode='lines', name='Close Price', line=dict(color='blue')))

    # Update layout
    fig.update_layout(title='Stock Price Chart',
                      xaxis_title='Date',
                      yaxis_title='Price',
                      template='plotly_white')

    # Display the plot in Streamlit
    st.plotly_chart(fig)

# Analyze news articles using Gemini AI
def analyze_news_with_gemini(alpha_news, sec_data, simfin_data, finnhub_data):
    combined_articles = []

    if alpha_news and isinstance(alpha_news, dict):
        for article in alpha_news.get("feed", []):
            if isinstance(article, dict):
                title = article.get("title", "No Title")
                summary = article.get("summary", "No summary available")
                combined_articles.append(f"Alpha Vantage: {title} - {summary}")

    # Add SEC data to the analysis
    if sec_data:
        combined_articles.append(f"SEC Data: {sec_data}")

    # Add Simfin data to the analysis
    if simfin_data:
        combined_articles.append(f"Simfin Data: {simfin_data}")

    # Add Finnhub data to the analysis
    if finnhub_data:
        combined_articles.append(f"Finnhub Data: {finnhub_data}")

    # Prepare prompt for AI analysis
    prompt = f"Analyze the following articles and provide detailed financial insights:\n\n" + "\n".join(combined_articles)

    try:
        response = model.generate_content(prompt)
        analysis_result = response.text
        return analysis_result
    except Exception as e:
        st.error(f"Error analyzing news with Gemini: {e}")
        return None

def main():
    st.title("Stock Market Analysis Agent")
    
    # Create tabs for analysis and chat
    tab1, tab2 = st.tabs(["Analysis", "Chat"])

    with tab1:
        st.header("Fetching News...")
        alpha_news = fetch_alpha_vantage_news()
        ticker = st.text_input("Enter Stock Ticker (e.g., AAPL):", "AAPL")
        
        # Fetch additional data
        finnhub_data = fetch_finnhub_data(ticker)
        sec_data = fetch_sec_data("0000320193")  # Example CIK for Apple Inc.
        simfin_data = fetch_simfin_data(ticker)
        polygon_data = fetch_polygon_data(ticker)

        st.header("Analyzing News...")
        analysis = analyze_news_with_gemini(alpha_news, sec_data, simfin_data, finnhub_data)

        # Display AI Analysis
        st.header("AI Analysis and Suggestions")
        st.write(analysis)

        # Fetch and analyze stock data
        if st.button("Fetch Stock Data"):
            stock_data = fetch_stock_data(ticker, "2023-01-01", "2024-12-31")
            analyze_chart(stock_data)

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