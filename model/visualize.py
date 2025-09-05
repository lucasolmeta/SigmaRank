from config import BASE_DIR
import os
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime

def main():
    RETURNS_PATH = os.path.join(BASE_DIR,'results','daily_returns.csv')
    returns = pd.read_csv(RETURNS_PATH)

    returns['Date'] = pd.to_datetime(returns['Date'])

    returns = returns.set_index('Date')

    returns.plot(y='Overall Return', kind='line')
    returns.plot(y='SPY Return', kind='line')

if __name__ == '__main__':
    main() 