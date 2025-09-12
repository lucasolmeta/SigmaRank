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

    schedule = nyse.schedule(
        start_date=now - pd.Timedelta(days=1),
        end_date=now + pd.Timedelta(days=7)
    ).reset_index()

    schedule['date'] = schedule['market_open'].dt.tz_convert(ny_tz).dt.normalize()

    today_date = pd.Timestamp(now.date(), tz=ny_tz)
    today_row = schedule.loc[schedule['date'] == today_date]

    if not today_row.empty and today_row['market_open'].iloc[0] <= now <= today_row['market_close'].iloc[0]:
        raise RuntimeError("Market is still open - please try again later")

    if not today_row.empty and now <= today_row['market_close'].iloc[0]:
        next_day = today_date.strftime('%Y-%m-%d')
    else:
        future_row = schedule.loc[schedule['date'] > today_date].iloc[0]
        next_day = future_row['date'].strftime('%Y-%m-%d')

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