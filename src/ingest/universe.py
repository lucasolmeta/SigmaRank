import yaml
import pandas as pd
import yfinance as yf
import requests
from io import StringIO
from src.utils.paths import get_yaml_path

YAML_PATH = get_yaml_path()
YAML_PATH_STR = get_yaml_path(format='str')

with open(YAML_PATH_STR) as f:
    config = yaml.safe_load(f)

def main():
    top_n = config['fetch']['number']
    lookback_period = config['fetch']['lookback_period']

    url = "https://en.wikipedia.org/wiki/List_of_S%26P_500_companies"
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0 Safari/537.36'}

    response = requests.get(url, headers=headers)
    response.raise_for_status()

    sp500_tickers = (
        pd.read_html(StringIO(response.text))[0]['Symbol']
        .astype(str)
        .str.upper()
        .str.replace('.', '-', regex=False)
        .tolist()
    )

    data = yf.download(' '.join(sp500_tickers), period=lookback_period, interval='1d', group_by='ticker')

    adv = {}
    multi = isinstance(data.columns, pd.MultiIndex)
    
    for ticker in sp500_tickers:
        try:
            df = data[ticker] if multi else data
            dv = (df['Close'] * df['Volume']).dropna()
            if len(dv): adv[ticker] = float(dv.mean())
        except Exception:
            pass

    tickers = [k for k,_ in sorted(adv.items(), key=lambda x: x[1], reverse=True)[:top_n]]

    config['fetch']['tickers'] = tickers
    YAML_PATH.write_text(yaml.safe_dump(config, sort_keys=False))

if __name__ == '__main__':
    main()