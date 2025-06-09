import yfinance as yf
import sys
import os
import pandas as pd

def main():
    # get ticker symbol list

    sys.path.append(os.path.abspath('..'))
    from config import ticker_symbols

    # fetch requested ticker data

    data = yf.download(ticker_symbols, period='max', interval='1d')
    os.makedirs('data/by_stock', exist_ok=True)

    # split each ticker into it's own file

    if isinstance(data.columns, pd.MultiIndex):
        for ticker in ticker_symbols:
            df = data.xs(ticker, axis=1, level=1, drop_level=False).droplevel(1, axis=1)
            df.to_csv(f'data/by_stock/{ticker}.csv')

            print(f'Data obtained for {ticker}')

    # fetch and save SPY data

    data = yf.download('SPY', period='max', interval='1d')
    df.to_csv(f'data/by_stock/SPY.csv')

if __name__ == "__main__":
    main()