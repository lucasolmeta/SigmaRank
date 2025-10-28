import yfinance as yf
import sys
import os
import pandas as pd
import shutil
from config import BASE_DIR
import yaml

def main():
    # get ticker symbol list

    sys.path.append(os.path.abspath('..'))
    from config import ticker_symbols

    #####################
    ### DATA FETCHING ###
    #####################

    # fetch requested ticker data

    data = yf.download(ticker_symbols, period='max', interval='1d')

    # clear / create directory

    DIR_PATH = os.path.join(BASE_DIR, 'data', 'by_stock')

    if os.path.exists(DIR_PATH):
        shutil.rmtree(DIR_PATH)
        os.makedirs(DIR_PATH)
    else:
        os.makedirs(DIR_PATH, exist_ok=True)

    # split each ticker into it's own file

    if isinstance(data.columns, pd.MultiIndex):
        for ticker in ticker_symbols:
            df = data.xs(ticker, axis=1, level=1, drop_level=False).droplevel(1, axis=1)

            TICKER_PATH = os.path.join(BASE_DIR, 'data', 'by_stock', f'{ticker}.csv')

            df.reset_index(inplace=True)
            df.to_csv(TICKER_PATH, index=False)

if __name__ == '__main__':
    main()