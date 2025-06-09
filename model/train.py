from xgboost import XGBRegressor
import sys
import os
import pandas as pd
from sklearn.metrics import mean_squared_error, r2_score
import numpy as np

def main():
    # get ticker symbol list

    sys.path.append(os.path.abspath('../'))
    from config import ticker_symbols

    for ticker in ticker_symbols:

        ######################
        ### MODEL TRAINING ###
        ######################

        # extract data

        data = pd.read_csv(f'by_stock/{ticker}.csv')

        # split data

        feature_columns = data.columns.difference(['target_daily_return'])

        train, test = data.iloc[:-60].copy(), data.iloc[-60:].copy()

        X_train, y_train = train[feature_columns], train['target_daily_return']
        X_test, y_test = test[feature_columns], test['target_daily_return']

        # train model

        model = XGBRegressor(n_estimators=100, max_depth=3, learning_rate=0.1)
        model.fit(X_train, y_train)

        # predict

        y_pred = model.predict(X_test)

        # evaluate

        rmse = np.sqrt(mean_squared_error(y_test, y_pred))
        r2 = r2_score(y_test, y_pred)

        print(f'{ticker} RMSE: {rmse:.5f}')
        print(f'{ticker} R² Score: {r2:.3f}')