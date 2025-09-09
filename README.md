# Portfolio-Tracker

A stock portfolio web application built with **Streamlit** in Python as part of a programming course at the University of St. Gallen.  

This app lets users:

- Create and manage a personal stock portfolio  
- Add or sell stocks  
- View a real-time overview of portfolio performance  
- Access detailed stock information (sector, market cap, valuation metrics, etc.)  
- Visualize historical price data with interactive charts  

---

## How to Run

1. Install the required dependencies:  
   ```bash
   pip3 install -r requirements.txt
Or manually:

pip3 install streamlit yfinance pandas plotly

2. Run the app:
   
streamlit run Current_Stock_Portfolio_Manager.py



The app will open in your browser at http://localhost:8501.

## Dependencies

- Streamlit – Web application framework
- yfinance – Retrieve real-time and historical financial data
- pandas – Data manipulation and portfolio management
- plotly – Interactive financial charts

## Features
- Add and remove tickers in your portfolio
- Fetch live market data directly from Yahoo Finance
- Display company information (sector, industry, P/E ratios, dividend yield, etc.)
- Visualize price history and portfolio evolution with interactive plots
- Store portfolio data locally in my_portfolio.csv

## Acknowledgments
- Yahoo Finance via the yfinance library
- The Streamlit team for the simple and powerful framework
- ChatGPT for inspiration and debugging help during development


