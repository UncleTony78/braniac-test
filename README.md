# Advanced Stock News Agent with Gemini 2.0

A Python agent that uses Google's Gemini 2.0 to analyze stock market news and sentiment from multiple professional data sources.

## Features
- Daily comprehensive market updates at 9:00 AM
- Multiple data sources integration:
  - Alpha Vantage (market news and sentiment)
  - Financial Modeling Prep (company-specific news)
  - Finnhub (market sentiment analysis)
- Advanced analysis using Gemini 2.0 providing:
  - Key market movements and sector trends
  - Important stock-related highlights
  - Market sentiment and outlook
  - Potential risks and opportunities

## Setup
1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Environment variables are already set up in `.env` file with your Gemini API key.

## Usage
Run the agent:
```bash
python stock_news_agent.py
```

The agent will:
- Start immediately with a comprehensive market analysis
- Schedule daily updates at 9:00 AM
- Provide detailed insights combining multiple data sources
- Output formatted analysis with actionable insights

## Data Sources
The agent uses multiple professional financial APIs:
- Alpha Vantage: General market news and sentiment
- Financial Modeling Prep: Company-specific news
- Finnhub: Market sentiment analysis

All API keys are pre-configured in the code.