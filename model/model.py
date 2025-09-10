from xgboost import XGBRegressor
import sys
import os
import pandas as pd
from config import BASE_DIR
from datetime import datetime, time
import pytz
from pandas_market_calendars import get_calendar

def main():
    # get ticker symbol list

    sys.path.append(os.path.abspath('../'))
    from config import ticker_symbols

    predictions = pd.DataFrame(columns=['Ticker','Predicted Return','Previous Close','Predicted Close', 'Recommended Action'])

    # determine date of next business day

    nyse = get_calendar('NYSE')
    ny_tz = pytz.timezone('America/New_York')
    now = datetime.now(tz=ny_tz)
    market_close_time = time(16, 30)

    schedule = nyse.schedule(
        start_date=now - pd.Timedelta(days=1),
        end_date=now + pd.Timedelta(days=7)
    )

    trading_days = schedule.index.tz_localize('UTC').tz_convert(ny_tz).normalize()
    today = pd.Timestamp(now.date(), tz=ny_tz)

    if today in trading_days and now.time() <= market_close_time:
        next_day = today.strftime('%Y-%m-%d')
    else:
        future_trading_days = trading_days[trading_days > today]
        next_day = future_trading_days[0].strftime('%Y-%m-%d')

    for ticker in ticker_symbols:

        if ticker == 'SPY':
            continue

        # extract data

        TICKER_PATH = os.path.join(BASE_DIR,'data','by_stock',f'{ticker}.csv')
        data = pd.read_csv(TICKER_PATH)

        #################################
        ### REGRESSION MODEL TRAINING ###
        #################################

        # split test and prediction data

        feature_columns = data.columns.difference(['target_daily_return','target_daily_result','Date'])

        train, test = data.iloc[:-1].copy(), data.iloc[-1:].copy()

        X_train, y_train = train[feature_columns], train['target_daily_return']
        X_test = test[feature_columns]

        # fit model

        model = XGBRegressor(n_estimators=100, max_depth=3, learning_rate=0.1)
        model.fit(X_train, y_train)

        # predict

        pred_return = model.predict(X_test)
        pred_return = pred_return[0] * 100

        # interpret results
        
        previous_close = float(data.iloc[-1]['previous_close'])
        pred_close = previous_close * (pred_return/100 + 1)

        ####################
        ### SAVE RESULTS ###
        ####################
        
        predictions.loc[len(predictions)] = {
            'Ticker': ticker,
            'Predicted Return': pred_return,
            'Previous Close': float(previous_close),
            'Predicted Close': float(pred_close),
            'Recommended Action': 'No Action'
        }

    predictions.sort_values(
        by=['Predicted Return'],
        ascending=[False],
        inplace=True
    )
    predictions.reset_index(drop=True, inplace=True)

    for i, row in predictions.iterrows():
        if i < 5:
            if row['Predicted Return'] > 0.3:
                predictions.loc[i, 'Recommended Action'] = 'Buy'
        else:
            break

    PRED_DIR = os.path.join(BASE_DIR, 'predictions')

    if not os.path.exists(PRED_DIR):
        os.makedirs(PRED_DIR, exist_ok=True)

    PRED_PATH = os.path.join(PRED_DIR, f'{next_day}-predictions.csv')
    predictions.to_csv(PRED_PATH, index=False)

if __name__ == '__main__':
    main() 