import sys
import os
import pandas as pd
from ta.trend import sma_indicator
from pandas.tseries.offsets import BDay
import numpy as np
from config import BASE_DIR

def main():
    # get ticker symbol list

    sys.path.append(os.path.abspath('../'))
    from config import ticker_symbols

    # extract SPY data

    SPY_PATH = os.path.join(BASE_DIR, 'data', 'by_stock', 'SPY.csv')
    spy_data = pd.read_csv(SPY_PATH)

    spy_data['Date'] = pd.to_datetime(spy_data['Date'])

    last_date = spy_data['Date'].max()
    next_date = last_date + BDay(1)

    # append prediction row to SPY df

    new_row = {col: np.nan for col in spy_data.columns}
    new_row['Date'] = pd.to_datetime(next_date)

    spy_data.loc[len(spy_data)] = new_row

    # SPY lagged return features

    spy_data['SPY_1d_lagged_return'] = spy_data['Close'].shift(1) / spy_data['Close'].shift(2) - 1
    spy_data['SPY_3d_lagged_return'] = spy_data['Close'].shift(1) / spy_data['Close'].shift(4) - 1
    spy_data['SPY_5d_lagged_return'] = spy_data['Close'].shift(1) / spy_data['Close'].shift(6) - 1

    # only include relevant SPY features

    spy_features = spy_data[[
        'Date',
        'SPY_1d_lagged_return',
        'SPY_3d_lagged_return',
        'SPY_5d_lagged_return',
    ]]

    for ticker in ticker_symbols:

        ###########################
        ### FEATURE ENGINEERING ###
        ###########################

        # extract pulled data

        TICKER_PATH = os.path.join(BASE_DIR, 'data','by_stock',f'{ticker}.csv')
        data = pd.read_csv(TICKER_PATH)        
        
        data['Date'] = pd.to_datetime(data['Date'])

        # append prediction row to ticker df

        last_date = data['Date'].max()
        next_date = last_date + BDay(1)

        new_row = {col: np.nan for col in data.columns}
        new_row['Date'] = pd.to_datetime(next_date)
    
        data.loc[len(data)] = new_row

        # merge df with SPY df

        data = pd.merge(data, spy_features, on='Date', how='left')

        # target features (tomorrow's daily return and result)

        data['target_daily_return'] = data['Close'] / data['Close'].shift(1) - 1
        data['target_daily_result'] = (data['target_daily_return'] > 0).astype(int)

        # previous day features
 
        data['previous_close'] = data['Close'].shift(1)
        data['previous_volume'] = data['Volume'].shift(1)

        # lagged return features

        data['1d_lagged_return'] = data['Close'].shift(1) / data['Close'].shift(2) - 1
        data['3d_lagged_return'] = data['Close'].shift(1) / data['Close'].shift(4) - 1
        data['5y_lagged_return'] = data['Close'].shift(1) / data['Close'].shift(6) - 1

        # volatility related features

        data['volatility_5d'] = data['Close'].pct_change(fill_method=None).shift(1).rolling(5).std()

        # volumn related features

        avg_volume_10 = data['Volume'].shift(2).rolling(10).mean()
        data['volume_spike_ratio'] = data['Volume'].shift(1) / avg_volume_10

        # return relative to SPY feature

        data['relative_3d_return'] = data['3d_lagged_return'] - data['SPY_3d_lagged_return']

        # sma10 features

        data['price_vs_sma10_ratio'] = data['previous_close'] / sma_indicator(data['previous_close'], window=10)
        data['sma5_vs_sma10_ratio'] = sma_indicator(data['previous_close'], window=5) / sma_indicator(data['previous_close'], window=10)

        # drop unnecessary features and incomplete observations

        data.drop(columns=['Close','High','Low','Open','Volume'], inplace=True)

        feature_columns = data.columns.difference(['target_daily_return'])
        data.dropna(subset=feature_columns, inplace=True)

        # save finalized data to csv

        data.to_csv(TICKER_PATH, index=False)        

if __name__ == '__main__':
    main()