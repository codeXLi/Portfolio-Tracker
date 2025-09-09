# Portfolio-Tracker
This project is a stock portfolio web application built with Streamlit in Python as part of a programming course at the University of St. Gallen.

The app allows users to:

Create and manage a personal stock portfolio.

Add or sell stocks.

View a real-time overview of portfolio performance.

Access detailed information about individual stocks (sector, market cap, valuation metrics, etc.).

Visualize historical price data with interactive charts.

.

How to Run

Install the required dependencies:

pip3 install -r requirements.txt


(or manually: pip3 install streamlit yfinance pandas plotly)

Run the app with:

streamlit run Current_Stock_Portfolio_Manager.py


The app will open in your browser at http://localhost:8501
.

Dependencies

Streamlit
: For building the web app.

yfinance
: Retrieve real-time and historical financial data.

pandas
: Data manipulation and portfolio management.

plotly
: Interactive financial charts.

Features

Add and remove tickers in your portfolio.

Fetch live market data directly from Yahoo Finance.

Display company information (sector, industry, P/E ratios, dividend yield, etc.).

Visualize price history and portfolio evolution with interactive plots.

Store portfolio data locally (my_portfolio.csv).

Acknowledgments

Yahoo Finance via the yfinance library.

Streamlit team for the simple and powerful web app framework.

ChatGPT as inspiration and debugging help during development.
