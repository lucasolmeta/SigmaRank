import sys
import os
import pandas as pd
from ta import add_all_ta_features

sys.path.append(os.path.abspath('..'))
from config import ticker_symbols

spy_data = pd.read_csv('by_stock/SPY.csv')
spy_data['Date'] = pd.to_datetime(spy_data['Date'])

spy_data['SPY_1_day_lagged_return_%'] = spy_data['Close'].shift(1) / spy_data['Close'].shift(2) - 1
spy_data['SPY_3_day_lagged_return_%'] = spy_data['Close'].shift(1) / spy_data['Close'].shift(4) - 1
spy_data['SPY_5_day_lagged_return_%'] = spy_data['Close'].shift(1) / spy_data['Close'].shift(6) - 1

spy_data['SPY_1_day_lagged_return_$'] = spy_data['Close'].shift(1) - spy_data['Close'].shift(2)
spy_data['SPY_3_day_lagged_return_$'] = spy_data['Close'].shift(1) - spy_data['Close'].shift(4)
spy_data['SPY_5_day_lagged_return_$'] = spy_data['Close'].shift(1) - spy_data['Close'].shift(6)

spy_features = spy_data[[
    'Date',
    'SPY_1_day_lagged_return_%',
    'SPY_3_day_lagged_return_%',
    'SPY_5_day_lagged_return_%',
    'SPY_1_day_lagged_return_$',
    'SPY_3_day_lagged_return_$',
    'SPY_5_day_lagged_return_$'
]]

for ticker in ticker_symbols:

    data = pd.read_csv(f'by_stock/{ticker}.csv')
    data['Date'] = pd.to_datetime(data['Date'])

    data.dropna(inplace=True)

    data['PreviousClose'] = data['Close'].shift(1)

    data['1_day_lagged_return_%'] = data['Close'].shift(1) / data['Close'].shift(2) - 1
    data['3_day_lagged_return_%'] = data['Close'].shift(1) / data['Close'].shift(4) - 1
    data['5_day_lagged_return_%'] = data['Close'].shift(1) / data['Close'].shift(6) - 1

    data['1_day_lagged_return_$'] = data['Close'].shift(1) - data['Close'].shift(2)
    data['3_day_lagged_return_$'] = data['Close'].shift(1) - data['Close'].shift(4)
    data['5_day_lagged_return_$'] = data['Close'].shift(1) - data['Close'].shift(6)

    data = pd.merge(data, spy_features, on='Date', how='left')

    '''data = add_all_ta_features(
        data,
        open="Open",
        high="High",
        low="Low",
        close="Close",
        volume="Volume",
        fillna=True
    )'''

    data.dropna(inplace=True)
    data.reset_index(drop=True, inplace=True)

    data.to_csv(f'by_stock/{ticker}.csv')