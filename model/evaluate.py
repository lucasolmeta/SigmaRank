import pandas as pd
import numpy as np
from datetime import datetime, time
from pandas_market_calendars import get_calendar
import os
from config import BASE_DIR
import pytz

def main():

    # determine date of last prediction and next business day

    nyse = get_calendar('NYSE')
    ny_tz = pytz.timezone('America/New_York')
    now = datetime.now(tz=ny_tz)

    schedule = nyse.schedule(
        start_date=now - pd.Timedelta(days=7),
        end_date=now + pd.Timedelta(days=7)
    ).reset_index()

    schedule['date'] = schedule['market_open'].dt.tz_convert(ny_tz).dt.normalize()

    today_date = pd.Timestamp(now.date(), tz=ny_tz)

    if not schedule.loc[schedule['date'] == today_date].empty and now <= schedule.loc[schedule['date'] == today_date]['market_close'].iloc[0]:
        completed_day = schedule.loc[schedule['date'] < today_date].iloc[-1]['date'].strftime('%Y-%m-%d')
    else:
        completed_day = today_date.strftime('%Y-%m-%d')

    # fetch predictions

    try:
        PRED_PATH = os.path.join(BASE_DIR, 'predictions', f'{completed_day}-predictions.csv')

        pred = pd.read_csv(PRED_PATH)
    except Exception as e:        
        PRED_PATH = os.path.join(BASE_DIR, 'predictions', f'{completed_day}-predictions.csv')

        raise Warning('Predictions file not found')
    
    # create results df
    
    results = pd.DataFrame(columns=['Ticker','Predicted Return','Return','Previous Close','Predicted Close', 'Close', 'Recommended Action'])

    for ticker in pred['Ticker']:
        # get data by ticker

        DATA_PATH = os.path.join(BASE_DIR, 'data', 'by_stock', f'{ticker}.csv')
        data = pd.read_csv(DATA_PATH)

        new_row = {
            'Ticker': ticker,
            'Predicted Return': pred[pred['Ticker'] == ticker]['Predicted Return'].iloc[0],
            'Return': (data.loc[len(data) - 1, 'previous_close'] / data.loc[len(data) - 2, 'previous_close'] - 1) * 100,
            'Previous Close': data.loc[len(data) - 2, 'previous_close'],
            'Predicted Close': pred[pred['Ticker'] == ticker]['Predicted Close'].iloc[0],
            'Close': data.loc[len(data) - 1, 'previous_close'],
            'Recommended Action': pred[pred['Ticker'] == ticker]['Recommended Action'].iloc[0]
        }

        results.loc[len(results)] = new_row

    results.reset_index(drop=True, inplace=True)

    TODAY_RESULTS_PATH = os.path.join(BASE_DIR, 'results', f'{completed_day}-results.csv')
    results.to_csv(TODAY_RESULTS_PATH)

    DAILY_RETURNS_PATH = os.path.join(BASE_DIR, 'results', 'daily-returns.csv')
    daily_returns = pd.read_csv(DAILY_RETURNS_PATH, index_col=False)

    daily_returns = daily_returns[['Date','Recommended Buys','Positive Returns','Negative Returns','Predicted Return','SPY Return','Overall Return']]

    recommended_buys = len(results[results['Recommended Action'] == 'Buy'])
    positive_returns = len(results[(results['Recommended Action'] == 'Buy') & (results['Return'] > 0)])
    negative_returns = len(results[(results['Recommended Action'] == 'Buy') & (results['Return'] < 0)])
    predicted_return = np.mean(results[results['Recommended Action'] == 'Buy']['Predicted Return'])
    sp_return = data.loc[len(data) - 1, 'SPY_1d_lagged_return'] * 100
    overall_return = float(np.mean(results[results['Recommended Action'] == 'Buy']['Return']))

    new_row = {
        'Date': completed_day,
        'Recommended Buys': recommended_buys,
        'Positive Returns': positive_returns,
        'Negative Returns': negative_returns,
        'Predicted Return': predicted_return,
        'SPY Return': sp_return,
        'Overall Return': overall_return
    }

    if completed_day in daily_returns['Date'].values:
        daily_returns.loc[daily_returns['Date'] == completed_day, :] = pd.DataFrame([new_row])
    else:
        daily_returns.loc[len(daily_returns)] = new_row
    
    daily_returns.to_csv(DAILY_RETURNS_PATH, index=False)

if __name__ == '__main__':
    main()