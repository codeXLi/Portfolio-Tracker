
################################################################################
## This app is a stock portfolio manager created by the CS-group 5.2.         ##
## If you have multiple stock brokers, this app comes in handy.               ##
## With it, you can consolidate all your owned stocks into a single portfolio ## 
## and monitor its performance, as well as retrieve useful                    ##
## information about companies and their stocks.                              ##
## The functionalities that this app provides are therefore as follows:       ##
## adding stock to the portfolio, removing sold stock from the portfolio,     ##
## displaying the portfolio and its performance, and retrieving stock data.   ##
## Be aware, before using this app, pip installing yfinance may be required.  ##
################################################################################

import streamlit as st
import yfinance as yf
import pandas as pd
from datetime import datetime
import plotly.graph_objects as go

# Function for loading or creating portfolio
def load_portfolio():
    
    # Try to load portfolio if file already exists
    try:
        portfolio = pd.read_csv('my_portfolio.csv')
        return pd.DataFrame(portfolio)
        
    # If file not found create new DataFrame with the respective columns
    except FileNotFoundError:
        return pd.DataFrame(columns=['Ticker', 'Avg. Purchase Price', 'Number of Stocks',])

# Load portfolio into variable portfolio
portfolio = load_portfolio() 

# Function for saving portfolio to .csv File
def save_portfolio(portfolio):
    portfolio.to_csv('my_portfolio.csv', index=False)
    

# Save portfolio
save_portfolio(portfolio) 

# Function for displaying stock data
def display_stock_data(ticker):
    
    # Fetch the stock information
    stock = yf.Ticker(ticker)
    info = stock.info

    # Display the company name as a header
    st.header(f"{info.get('longName', ticker)}")

    # Display current market price
    st.metric(label="Current Price", value=f"${info.get('currentPrice', 'N/A')}")

    # Get today's date in YYYY-MM-DD format (as expected by yfinance)
    end_date = datetime.now().strftime('%Y-%m-%d')
    
    # Fetch historical stock data since 2021
    stock_hist = stock.history(start='2021-01-01', end=end_date)

    # Plot the historical closing prices
    st.line_chart(stock_hist['Close'])

    # Display additional financial information
    st.subheader("Overview of Stock Information, Financials, and Market Performance:")
    st.write(f"**Company:** {info.get('longName', 'N/A')}")
    st.write(f"**Symbol:** {info.get('symbol', 'N/A')}")
    st.write(f"**Exchange:** {info.get('exchange', 'N/A')}")
    st.write(f"**Currency:** {info.get('currency', 'N/A')}")
    st.write(f"**Sector:** {info.get('sector', 'N/A')}")
    st.write(f"**Industry:** {info.get('industry', 'N/A')}")
    st.write(f"**Country:** {info.get('country', 'N/A')}")
    st.write(f"**Market Cap:** {info.get('marketCap', 'N/A')}")
    st.write(f"**Forward PE:** {info.get('forwardPE', 'N/A')}")
    st.write(f"**Trailing PE:** {info.get('trailingPE', 'N/A')}")
    st.write(f"**Price to Sales (TTM):** {info.get('priceToSalesTrailing12Months', 'N/A')}")
    st.write(f"**Dividend Rate:** {info.get('dividendRate', 'N/A')}")
    st.write(f"**Trailing Annual Dividend Yield:** {info.get('trailingAnnualDividendYield', 'N/A')}")
    st.write(f"**Trailing Annual Dividend Rate:** {info.get('trailingAnnualDividendRate', 'N/A')}")
    st.write(f"**Earnings Quarterly Growth:** {info.get('earningsQuarterlyGrowth', 'N/A')}")
    st.write(f"**Revenue Growth:** {info.get('revenueGrowth', 'N/A')}")

# Function for validating the Ticker that was inputed by the User
def validate_ticker(ticker):

    # Check if user entered something in Ticker field
    if ticker != '':
        
        # Fetch the stock information            
        stock = yf.Ticker(ticker)
        info = stock.info
    
        # Check fetched stock information (if ticker doesn't exist 'trailingPegRatio' = None)
        if info['trailingPegRatio'] != None:
            return True

        else:
            # Tell user to input a valid Ticker
            st.warning('Please enter a valid ticker.')
            return False
    
    else: 
        # If user did not enter anything in ticker field return False
        return False

# Function for adding stock to portfolio
def add_stock(ticker, purchase_price, num_stocks):  

    # Check if purchase price the user inputed is above 0 
    if purchase_price != 0:
        
        # Globalize the portfolio variable
        global portfolio

        # Check if added stock already exists in portfolio
        if ticker in portfolio['Ticker'].values:
        
            # Get the old number of stocks and old avg. purchase price of stock
            old_num_stocks = portfolio.loc[portfolio['Ticker'] == ticker, 'Number of Stocks'].values[0]
            old_avg_price = portfolio.loc[portfolio['Ticker'] == ticker, 'Avg. Purchase Price'].values[0]
        
            # Calculate new number of stocks and new avg. purchase price of stock
            new_num_stocks = old_num_stocks + num_stocks
            new_avg_price = ((old_avg_price * old_num_stocks) + (purchase_price * num_stocks)) / new_num_stocks
            

            # Set new number of stocks and new avg. purchasse price 
            portfolio.loc[portfolio['Ticker'] == ticker, 'Number of Stocks'] = new_num_stocks
            portfolio.loc[portfolio['Ticker'] == ticker, 'Avg. Purchase Price'] = new_avg_price
        
            # Save updated portfolio to .csv File
            save_portfolio(portfolio)
        

        # If added stock doesn't exist in portfolio 
        else:
            # Create new entry in the portfolio
            new_row = pd.DataFrame({'Ticker': ticker, 'Avg. Purchase Price': purchase_price,'Number of Stocks': num_stocks}, index=[0])

            # Save new entry to .csv file
            with open('my_portfolio.csv', 'a') as f:
                new_row.to_csv(f, header=False, index=False)

        # Tell User that he added stock to Portfolio
        st.success(f"Added {num_stocks} stocks of {ticker} at ${purchase_price} per share to your portfolio.") 

    else: 
        # If purchase price not above 0 tell user that it has to be above 0
        st.warning('Purchase price has to be above 0$.')

# Function for removing sold stock form the portfolio
def remove_sold_stock(ticker, num_stocks_sold):

    # Check if user selected an option in ticker field
    if ticker != None:   
        
        # Get number of stocks 
        num_stocks = portfolio.loc[portfolio['Ticker'] == ticker, 'Number of Stocks']
    
        # Calculate new number of stocks
        new_num_stocks = num_stocks - num_stocks_sold
    
        # Set new number of stocks 
        portfolio.loc[portfolio['Ticker'] == ticker, 'Number of Stocks'] = new_num_stocks

        # If new number of stocks reaches 0 delete entry
        if int(new_num_stocks.iloc[0]) == 0:
        
            # Set ticker as index
            portfolio.set_index('Ticker', inplace=True)
        
            # Drop row with ticker in it
            portfolio.drop(ticker, axis=0,inplace=True)
        
            # Reset index
            portfolio.reset_index(inplace=True)

        # Save updated portfolio to .csv
        save_portfolio(portfolio)

        # Tell user how much stock was removed from the portfolio
        st.success(f'Removed {num_stocks_sold} stocks of {ticker} from your portfolio.')


# Function for displaying total portfolio value
def display_portfolio():

    # Check if portfolio is empty
    if not portfolio.empty:
    
        # Get current price of stock in new column
        portfolio['Current Price'] = portfolio['Ticker'].apply(lambda x: yf.Ticker(x).history(period='1d')['Close'][0])
        
        # Calculate total value of stock in new column
        portfolio['Total Value'] = portfolio['Number of Stocks'] * portfolio['Current Price']
        
        # Calculate total gain/loss of stock in new column
        portfolio['Total Gain/Loss'] = (portfolio['Current Price'] - portfolio['Avg. Purchase Price']) * portfolio['Number of Stocks']
        
        # Calculate percentage change of stock in new column
        portfolio['Percentage Change'] = (portfolio['Total Gain/Loss'] / (portfolio['Avg. Purchase Price'] * portfolio['Number of Stocks'])) * 100
        
        # Calculate total percentage change
        total_percentage_change = portfolio['Percentage Change'].sum()
                
        # Sort portfolio based on Ticker (for alphabetical display)
        portfolio.sort_values('Ticker', inplace= True)
        
        # Style portfolio with different colors for total gain/loss and percentage change depending on their values. As well as formatting avg. purchase price, percentage change, total gain/loss current price so they look cleaner 
        styled_portfolio = portfolio.style.applymap(lambda x: 'color: green' if x > 0 else ('color: red' if x < 0 else 'color: white'), subset=['Total Gain/Loss', 'Percentage Change']).format({'Avg. Purchase Price': '{:.2f}$','Percentage Change': '{:.1f}%', 'Total Gain/Loss': '{:.2f}$', 'Current Price': '{:.2f}$','Total Value': '{:.2f}$'})
        
        # Display styled portfolio in streamlit
        st.dataframe(styled_portfolio,hide_index=True)

        # Create a list of colors corresponding to the values of percentage change for the plot 
        colors = ['green' if value > 0 else ('red' if value < 0 else 'white') for value in portfolio['Percentage Change']]

        # Create the purchase change plot with xaxis = ticker and y axis = percentage change and applying the colors 
        purchase_change_plot = go.Figure(go.Bar(x=portfolio['Ticker'], y=portfolio['Percentage Change'],marker_color= colors))

        # Add titles to the purchase change plot
        purchase_change_plot.update_layout(title="Stock performance",xaxis_title="Ticker",yaxis_title="Percentage Change",)

        # Plot the plot in streamlit
        st.plotly_chart(purchase_change_plot)

        # Get the correct color for the total percentage change 
        total_percentage_change_color = 'green' if total_percentage_change > 0 else ('red' if total_percentage_change < 0 else 'white')

        # Display the total percentage change in streamlit
        st.write(f'**Total Portfolio Percentage Change**: :{total_percentage_change_color}[{total_percentage_change:.1f}%]')

    # If portfolio is empty
    else:
        # Tell user his portfolio is empty
        st.write("Your Portfolio is empty.")


# Main streamlit interface

# Name of app as sidebar title
st.sidebar.title('Stock Portfolio Manager')

# Create app mode for navigation between the different functions of the app
app_mode = st.sidebar.selectbox('Choose the option', ['View Portfolio', 'Add Stock', 'Remove Sold Stock', 'Check Stock Data'])

# If app mode add stock is selected
if app_mode == 'Add Stock':
    
    # Add a streamlit header
    st.header('Add New Stock to Portfolio')

    # Create a streamlit form 
    with st.form('Stock Input'):

        # Get ticker from user with stremlit text input
        new_ticker = st.text_input('Ticker').upper()

        # Get purchase price from user with streamlit number input
        new_purchase_price = st.number_input('Purchase Price', min_value=0.0, format='%.2f')

        # Get number of stocks user wants to add form user with streamlit number input
        new_num_stocks = st.number_input('Number of Stocks', min_value=1, step=1)
        
        # Ceate submit form button 
        submitted = st.form_submit_button('Add Stock')

        # If user presses submit button
        if submitted:
            
            # Check if ticker is valid
            if validate_ticker(new_ticker):
                
                # If ticker valid add stock 
                add_stock(new_ticker, new_purchase_price, new_num_stocks,)
                
# If app mode remove sold stock is selected                  
elif app_mode == 'Remove Sold Stock':

    # Add a streamlit header
    st.header('Remove Sold Stock from Portfolio')

    # Create a streamlit form
    with st.form('Stock Input'):

        # Get ticker via streamlit selectbox (user can only select tickers that are in his portfolio)
        ticker = st.selectbox('Ticker', portfolio['Ticker'], placeholder='Choose a Stock', index=None)   

        # Create submit button for confirming ticker selection
        st.form_submit_button('Confirm Selection')   
      
        # Set max number input value for number of stocks sold based on remaining number of stocks in portfolio
        max_num_input_value = portfolio.loc[portfolio['Ticker'] == ticker, 'Number of Stocks'].sum()
                        
        # Get number of stocks sold from user with streamlit number input while limiting number that can be choosen to number of respective stocks
        num_stocks_sold = st.number_input('Number of Stocks', min_value=0, max_value= max_num_input_value, step=1 ) 

        # Create form submit button 
        submitted = st.form_submit_button('Remove Stock')

        # If user presses submit button
        if submitted: 

            # Remove sold stock
            remove_sold_stock(ticker, num_stocks_sold)
           
# If app mode view portfolio is selected
elif app_mode == 'View Portfolio':

    # Add a streamlit header
    st.header('Current Portfolio')

    # Display portfolio
    display_portfolio()

# If app mode check stock data is selected
elif app_mode == 'Check Stock Data':

    # Add a streamlit header
    st.header('Check Stock Data')

    # Get ticker from user with streamlit text input
    ticker_to_check = st.text_input('Enter ticker to display data')

    # Create button 
    if st.button('Display Data'):

        # Check if ticker is valid
        if validate_ticker(ticker_to_check):
            # if ticker valid display stokc data
            display_stock_data(ticker_to_check)



#The code is mainly based on our acquired knowledge during the computer science class and these 3 sources: 
#https://pypi.org/project/yfinance/
#https://streamlit.io/
#https://plotly.com/python-api-reference/plotly.graph_objects.html#graph-objects
