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

    data = yf.download(tickers, period='max', interval='1d')

    # split each ticker into it's own file

    if isinstance(data.columns, pd.MultiIndex):
        for ticker in tickers:
            df = data.xs(ticker, axis=1, level=1, drop_level=False).droplevel(1, axis=1)

            if len(df) > days + 20:
                df = df[-(days + 20):]

            TICKER_PATH = os.path.join(DATA_DIR, 'raw', f'{ticker}.csv')

            df.reset_index(inplace=True)
            df.to_csv(TICKER_PATH, index=False)

if __name__ == '__main__':
    main()