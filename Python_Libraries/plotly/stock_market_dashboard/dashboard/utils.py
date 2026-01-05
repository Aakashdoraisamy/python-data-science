import yfinance as yf
import pandas as pd
import numpy as np

def fetch_stock_data(tickers, start="2023-01-01", end="2026-01-01"):
    """
    Fetch stock data for given tickers from Yahoo Finance.
    Returns a dictionary of DataFrames.
    """
    stock_data = {}
    for ticker in tickers:
        df = yf.download(ticker, start=start, end=end)
        df.reset_index(inplace=True)
        stock_data[ticker] = df
    return stock_data

def calculate_moving_average(df, column='Close', window=20):
    """Calculate moving average for a given column in DataFrame."""
    return df[column].rolling(window=window).mean()

def calculate_daily_return(df, column='Close'):
    """Calculate daily return percentage for a given column."""
    return df[column].pct_change() * 100
