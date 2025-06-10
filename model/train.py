from xgboost import XGBRegressor
import sys
import os
import pandas as pd
from sklearn.metrics import mean_squared_error, r2_score
import numpy as np


def main():
    # get ticker symbol list

    console = Console()

    sys.path.append(os.path.abspath('../'))
    from config import ticker_symbols

    for ticker in ticker_symbols:

        ######################
        ### MODEL TRAINING ###
        ######################

        if ticker == 'SPY':
            continue

        # extract data

        data = pd.read_csv(f'data/by_stock/{ticker}.csv')

        # split data

        feature_columns = data.columns.difference(['target_daily_return','Date'])

        train, test = data.iloc[:-1].copy(), data.iloc[-1:].copy()

        X_train, y_train = train[feature_columns], train['target_daily_return']
        X_test = test[feature_columns]

        # train model

        model = XGBRegressor(n_estimators=100, max_depth=3, learning_rate=0.1)
        model.fit(X_train, y_train)

        # predict

        y_pred = model.predict(X_test)
        result = y_pred[0]
        per_result = result * 100
        final = round(per_result, 2)

        print(f'Tomorrows predicted return for {ticker}: ' + str(final) + '%')
