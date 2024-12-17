# 📈 Stock Market Analysis Agent

Welcome to the **Stock Market Analysis Agent**! This project is designed to fetch and analyze stock market data using various financial APIs. The application provides insights based on real-time data, news articles, and historical stock prices, all while offering an interactive user experience through Streamlit.

## 🚀 Features

- **Real-Time Market Data**: Fetch real-time stock prices and market data using [Finnhub](https://finnhub.io).
- **News Analysis**: Retrieve and analyze financial news from [Alpha Vantage](https://www.alphavantage.co).
- **Filings from SEC**: Access company filings and reports from the [SEC](https://www.sec.gov).
- **Market Data from Polygon.io**: Get comprehensive market data for stocks, indices, currencies, and options from [Polygon.io](https://polygon.io).
- **Interactive Charts**: Visualize stock data with interactive charts using [Plotly](https://plotly.com).
- **AI Insights**: Use Google Gemini AI to analyze news articles and provide detailed financial insights.

## 🛠️ Technologies Used

- **Python**: Programming language for backend logic.
- **Streamlit**: Framework for creating interactive web applications.
- **yFinance**: Library for fetching historical stock data.
- **Plotly**: Library for creating interactive charts.
- **Requests**: Library for making HTTP requests to APIs.
- **dotenv**: For loading environment variables securely.

## 📦 Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/stock-market-analysis-agent.git
   cd stock-market-analysis-agent

2. Create a virtual environment (optional but recommended):
   python -m venv venv
.\venv\Scripts\activate  # On Windows
# source venv/bin/activate  # On macOS/Linux

3. Install dependencies:
   pip install -r requirements.txt

4. Set API keys in the `.env` file (or as environment variables).
   Copy the template `.env.example` to `.env` and update with your keys.
   GOOGLE_API_KEY=your_google_api_key
ALPHA_VANTAGE_KEY=your_alpha_vantage_key
FINHUB_KEY=your_finnhub_key
SEC_API_KEY=your_sec_api_key
SIMFIN_KEY=your_simfin_key
POLYGON_KEY=your_polygon_key

5. Run the application:
   streamlit run stock_market_analysis_agent.py

   📖 Contributing
Contributions are welcome! If you have suggestions or improvements, please open an issue or submit a pull request.

📄 License
This project is licensed under the MIT License - see the LICENSE file for details.

📞 Contact
For any inquiries, please reach out to [nwakezeanthony@gmail.com].

Thank you for checking out the Stock Market Analysis Agent! Happy analyzing! 🚀