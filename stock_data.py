#!/usr/bin/env python3

import yfinance as yf
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import plotly.io as pio

# Set Plotly theme to dark
pio.templates.default = "plotly_dark"

def fetch_stock_data(ticker, period="1y"):
    """
    Fetch stock data for a given ticker symbol
    
    Parameters:
    ticker (str): Stock ticker symbol
    period (str): Time period to fetch (default: "1y" for one year)
    
    Returns:
    pandas.DataFrame: Stock data
    """
    stock = yf.Ticker(ticker)
    data = stock.history(period=period)
    return data

def plot_stock_data(data, ticker):
    """
    Plot stock data with all metrics using Plotly
    
    Parameters:
    data (pandas.DataFrame): Stock data
    ticker (str): Stock ticker symbol
    """
    # Create figure with secondary y-axis
    fig = make_subplots(rows=2, cols=1, 
                       shared_xaxes=True,
                       vertical_spacing=0.05,
                       row_heights=[0.7, 0.3],
                       subplot_titles=(f'{ticker} Stock Price', 'Trading Volume'))

    # Add candlestick chart
    fig.add_trace(go.Candlestick(x=data.index,
                                open=data['Open'],
                                high=data['High'],
                                low=data['Low'],
                                close=data['Close'],
                                name='OHLC',
                                increasing_line_color='#26a69a',
                                decreasing_line_color='#ef5350',
                                hoverinfo='all'),
                  row=1, col=1)

    # Add volume bar chart
    colors = ['#ef5350' if row['Open'] > row['Close'] else '#26a69a' 
              for index, row in data.iterrows()]
    
    fig.add_trace(go.Bar(x=data.index,
                        y=data['Volume'],
                        name='Volume',
                        marker_color=colors,
                        opacity=0.7,
                        hovertemplate="Date: %{x}<br>Volume: %{y:,}<extra></extra>"),
                  row=2, col=1)

    # Add moving averages
    for window, color in [(50, '#FF9800'), (252, '#2196F3')]:  # 50-day and 52-week (252 trading days) MA
        if len(data) >= window:
            ma = data['Close'].rolling(window=window).mean()
            fig.add_trace(go.Scatter(x=data.index, 
                                   y=ma,
                                   name=f'{window} Day MA',
                                   line=dict(color=color, width=1.5),
                                   opacity=0.8,
                                   hovertemplate="Date: %{x}<br>MA: $%{y:.2f}<extra></extra>"),
                         row=1, col=1)

    # Update layout
    fig.update_layout(
        title=dict(
            text=f'{ticker} Stock Analysis (1 Year)',
            y=0.95,
            x=0.5,
            xanchor='center',
            yanchor='top',
            font=dict(size=24, color='white')
        ),
        height=900,
        template='plotly_dark',
        showlegend=True,
        legend=dict(
            yanchor="top",
            y=0.99,
            xanchor="left",
            x=0.01,
            bgcolor='rgba(0, 0, 0, 0.5)',
            bordercolor='rgba(255, 255, 255, 0.2)',
            borderwidth=1
        ),
        margin=dict(l=50, r=50, t=100, b=50),
        font=dict(family="Arial", size=12, color='white'),
        plot_bgcolor='black',
        paper_bgcolor='black',
        xaxis_rangeslider_visible=False
    )

    # Update y-axes
    fig.update_yaxes(
        title_text="Price (USD)",
        row=1,
        col=1,
        title_font=dict(size=14, color='white'),
        gridcolor='#333333',
        zerolinecolor='#333333'
    )
    
    fig.update_yaxes(
        title_text="Volume",
        row=2,
        col=1,
        title_font=dict(size=14, color='white'),
        gridcolor='#333333',
        zerolinecolor='#333333'
    )

    # Update x-axes
    fig.update_xaxes(
        gridcolor='#333333',
        zerolinecolor='#333333',
        showgrid=True,
        showline=True,
        linewidth=1,
        linecolor='#333333'
    )

    # Show the plot
    fig.show()

if __name__ == "__main__":
    while True:
        print("\n" + "="*50)
        print("Stock Data Analysis Tool")
        print("="*50)
        print("Enter 'q' or 'quit' to exit the program")
        
        ticker = input("\nEnter the stock ticker symbol: ").strip().upper()
        
        if ticker.lower() in ['q', 'quit']:
            print("\nThank you for using the Stock Data Analysis Tool!")
            break
            
        try:
            data = fetch_stock_data(ticker)
            if data.empty:
                print(f"\nNo data found for ticker symbol: {ticker}")
                continue
                
            print(f"\nFetched {len(data)} days of data for {ticker}")
            print("\nFirst few rows of data:")
            print(data.head())
            
            # Plot the data
            plot_stock_data(data, ticker)
            
        except Exception as e:
            print(f"\nError fetching data for {ticker}: {str(e)}")
            print("Please check if the ticker symbol is correct and try again.") 