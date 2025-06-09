import yfinance as yf
import sys
import os
import pandas as pd

sys.path.append(os.path.abspath('..'))
from config import ticker_symbols

data = yf.download(ticker_symbols, period='max', interval='1d')

os.makedirs('by_stock', exist_ok=True)

if isinstance(data.columns, pd.MultiIndex):
    for ticker in ticker_symbols:
        df = data.xs(ticker, axis=1, level=1, drop_level=False).droplevel(1, axis=1)
        df.to_csv(f'by_stock/{ticker}.csv')
        print(f'Saved {ticker}.csv — shape: {df.shape}')

data = yf.download('SPY', period='max', interval='1d')
df.to_csv(f'by_stock/SPY.csv')