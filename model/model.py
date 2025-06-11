from xgboost import XGBClassifier, XGBRegressor
import sys
import os
import pandas as pd
from config import BASE_DIR

def main():
    # get ticker symbol list

    sys.path.append(os.path.abspath('../'))
    from config import ticker_symbols

    predictions = pd.DataFrame(columns=['Ticker','Predicted Outcome','Outcome Certainty','Predicted Return','Recommendation','Previous Close','Predicted Close'])

    for ticker in ticker_symbols:

        if ticker == 'SPY':
            continue

        # extract data

        TICKER_PATH = os.path.join(BASE_DIR,'data',f'by_stock',f'{ticker}.csv')
        data = pd.read_csv(TICKER_PATH)

        date = str(data.iloc[-1]['Date'])

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

        #####################################
        ### CLASSIFICATION MODEL TRAINING ###
        #####################################

        # split test and prediction data

        feature_columns = data.columns.difference(['target_daily_return','target_daily_result','Date'])

        train, test = data.iloc[:-1].copy(), data.iloc[-1:].copy()

        X_train, y_train = train[feature_columns], train['target_daily_result']
        X_test = test[feature_columns]

        # fit model

        model = XGBClassifier(n_estimators=100, max_depth=3, learning_rate=0.1)
        model.fit(X_train, y_train)

        # predict

        probs = model.predict_proba(X_test)
        certainty = probs[:, 1][0]

        # interpret results

        result, recommendation = '',''
        
        if certainty > 0.5:
            result = '+'
            if certainty > 0.7:
                recommendation = 'Buy'
            else:
                recommendation = 'Refrain'
        else:
            result = '-'
            recommendation = 'Refrain'
            certainty = 1 - certainty

        ####################
        ### SAVE RESULTS ###
        ####################
        
        predictions.loc[len(predictions)] = {
            'Ticker': ticker,
            'Predicted Outcome': result,
            'Outcome Certainty': certainty,
            'Predicted Return': pred_return,
            'Recommendation': recommendation,
            'Previous Close': float(previous_close),
            'Predicted Close': float(pred_close)
        }

    predictions.sort_values(
        by=['Recommendation', 'Predicted Return'],
        ascending=[True, False],
        inplace=True
    )

    predictions.reset_index(drop=True, inplace=True)

    RESULTS_DIR = os.path.join(BASE_DIR, 'results')

    if not os.path.exists(RESULTS_DIR):
        os.makedirs(RESULTS_DIR, exist_ok=True)

    RESULTS_PATH = os.path.join(BASE_DIR, 'results', f'{date}-results.csv')
    predictions.to_csv(RESULTS_PATH, index=False)   

if __name__ == '__main__':
    main() 