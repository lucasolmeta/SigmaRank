import os
import pandas as pd
import numpy as np
from src.utils.paths import get_yaml, get_data_dir

config = get_yaml()

DATA_DIR = get_data_dir()

def main():
    # get ticker symbol list

    tickers = config['fetch']['tickers']

    for ticker in tickers:
        # extract pulled data

        RAW_TICKER_PATH = os.path.join(DATA_DIR, 'interim',f'{ticker}.csv')
        data = pd.read_csv(RAW_TICKER_PATH)        
        
        data['Date'] = pd.to_datetime(data['Date'])

        #Core Wyckoff effort/result metrics (effort = volume, result = movement)
        data['true range'] = (data['High'] - data['Low']).abs() # measures result, movement range for the day
        data['close_change'] = data['Close'].pct_change(fill_method=None)
        data['vol_sma_10'] = data['Volume'].shift(1).rolling(10).mean() # measures effort, rolling mean
        data['tr_sma_10'] = data['true range'].shift(1).rolling(10).mean() # measures result, rolling mean
        
        #Effort and result ratios
        tr_safe = data['true range'].replace(0, np.nan)
        data['effort_per_tr'] = data['Volume'] / tr_safe
        data['effort_per_tr_sma_10'] = data['effort_per_tr'].shift(1).rolling(10).mean() #normalize effort by 10_day_mean

        #Effort vs result ratio
        data['effort_vs_result'] = (data['Volume'] / data['vol_sma_10']) / (data['true range'] / data['tr_sma_10']) # (Volume / avg_10day_volume) / (true_range / avg_10day_true_range)

        data.to_csv(RAW_TICKER_PATH, index=False)
