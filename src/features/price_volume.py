import sys
import os
import pandas as pd
from ta.trend import sma_indicator
import numpy as np
from src.utils.paths import get_yaml, get_data_dir
from src.utils.dates import next_n_sessions

config = get_yaml()

DATA_DIR = get_data_dir()

def main():
    # get ticker symbol list

    tickers = config['fetch']['tickers']


    for ticker in tickers:

        # extract pulled data

        RAW_TICKER_PATH = os.path.join(DATA_DIR, 'raw',f'{ticker}.csv')
        data = pd.read_csv(RAW_TICKER_PATH)        
        
        data['Date'] = pd.to_datetime(data['Date'])

        # append prediction row to ticker df

        next_date = next_n_sessions(1)[0]

        new_row = {col: np.nan for col in data.columns}
        new_row['Date'] = pd.to_datetime(next_date.date())
    
        data.loc[len(data)] = new_row

        # target features (tomorrow's daily return and result)

        data['target_daily_return'] = data['Close'] / data['Close'].shift(1) - 1

        # previous day features
 
        data['previous_close'] = data['Close'].shift(1)
        data['previous_volume'] = data['Volume'].shift(1)

        # lagged return features

        data['1d_lagged_return'] = data['Close'].shift(1) / data['Close'].shift(2) - 1
        data['3d_lagged_return'] = data['Close'].shift(1) / data['Close'].shift(4) - 1
        data['5d_lagged_return'] = data['Close'].shift(1) / data['Close'].shift(6) - 1

        # volatility related features

        data['volatility_5d'] = data['Close'].pct_change(fill_method=None).shift(1).rolling(5).std()

        # volume related features

        avg_volume_10 = data['Volume'].shift(1).rolling(10).mean()
        data['volume_spike_ratio'] = data['Volume'].shift(1) / avg_volume_10

        # sma10 features

        data['price_vs_sma10_ratio'] = data['previous_close'] / sma_indicator(data['previous_close'], window=10)
        data['sma5_vs_sma10_ratio'] = sma_indicator(data['previous_close'], window=5) / sma_indicator(data['previous_close'], window=10)

        # drop unnecessary features / incomplete observations and finalize length

        num_rows = config['fetch']['days']
        data = data[-num_rows:]

        non_null_feats = data.columns.difference([
            'Date', 'Open', 'High', 'Low', 'Close', 'Volume', 'target_daily_return'
        ])
        data.dropna(subset=non_null_feats, inplace=True)

        # save finalized data to csv

        INT_TICKER_PATH = os.path.join(DATA_DIR, 'interim',f'{ticker}.csv')
        data.to_csv(INT_TICKER_PATH, index=False)        

if __name__ == '__main__':
    main()