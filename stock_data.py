import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

def fetch_stock_data(ticker, period="1mo"):
    """
    Fetch stock data for a given ticker symbol
    
    Parameters:
    ticker (str): Stock ticker symbol
    period (str): Time period to fetch (default: "1mo" for one month)
    
    Returns:
    pandas.DataFrame: Stock data
    """
    stock = yf.Ticker(ticker)
    data = stock.history(period=period)
    return data

def plot_stock_data(data, ticker):
    """
    Plot stock data with closing prices
    
    Parameters:
    data (pandas.DataFrame): Stock data
    ticker (str): Stock ticker symbol
    """
    plt.figure(figsize=(12, 6))
    sns.set_style("darkgrid")
    plt.plot(data.index, data['Close'], label='Closing Price')
    plt.title(f'{ticker} Stock Price')
    plt.xlabel('Date')
    plt.ylabel('Price (USD)')
    plt.legend()
    plt.show()

if __name__ == "__main__":
    # Example: Fetch and plot Apple stock data
    ticker = input("Enter the stock ticker symbol: ")
    data = fetch_stock_data(ticker)
    print(f"\nFetched {len(data)} days of data for {ticker}")
    print("\nFirst few rows of data:")
    print(data.head())
    
    # Plot the data
    plot_stock_data(data, ticker) 