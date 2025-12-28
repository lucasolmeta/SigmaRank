import yfinance as yf
import os
import pandas as pd
import yaml
from src.utils.paths import get_yaml, get_config_dir, get_data_dir, get_yaml_path

config = get_yaml()

YAML_PATH_STR = get_yaml_path(format='str')
CONFIG_DIR = get_config_dir()
DATA_DIR = get_data_dir()

def main():
    tickers = config['fetch']['tickers']
    days = config['fetch']['days']
    
    # Ensure tickers is a list
    if isinstance(tickers, str):
        tickers = [tickers]

    # Ensure raw directory exists
    raw_dir = DATA_DIR / 'raw'
    raw_dir.mkdir(parents=True, exist_ok=True)

    data = yf.download(tickers, period='max', interval='1d', group_by='ticker')

    # split each ticker into it's own file

    if isinstance(data.columns, pd.MultiIndex):
        for ticker in tickers:
            df = data.xs(ticker, axis=1, level=1, drop_level=False).droplevel(1, axis=1)

            if len(df) > days + 20:
                df = df[-(days + 20):]

            TICKER_PATH = raw_dir / f'{ticker}.csv'

            df.reset_index(inplace=True)
            df.to_csv(str(TICKER_PATH), index=False)

if __name__ == '__main__':
    main()