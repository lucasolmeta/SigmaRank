from datetime import datetime, timedelta
import pandas as pd
import pandas_market_calendars as mcal
from zoneinfo import ZoneInfo

EASTERN = ZoneInfo('America/New_York')
UTC = ZoneInfo('UTC')

def get_calendar(name='XNYS'):
    return mcal.get_calendar(name)

def trading_sessions(back_days: int, for_days: int=1, cal_name: str='XNYS'):
    if back_days < 0 or for_days < 0:
        raise RuntimeError(f'back_days and for_days must be non-negative!')
    elif back_days == 0 and for_days == 0:
        raise RuntimeError(f'back_days and for_days cannot both be zero!')

    cal = get_calendar(name=cal_name)

    now_et = datetime.now(tz=EASTERN)

    sched = cal.schedule(
        start_date=(now_et.date() - timedelta(days=back_days*3)),
        end_date=(now_et.date() + timedelta(days=for_days*3))
    )

    closes_et = pd.DatetimeIndex(sched['market_close'])

    past = closes_et[closes_et <= now_et]
    past = past.tail(back_days) if back_days > 0 else past[:0]

    future = closes_et[closes_et > now_et]
    future = future.head(for_days) if for_days > 0 else future[:0]

    sessions_et = pd.DatetimeIndex(pd.concat([past, future]))
    return sessions_et.tz_convert('UTC')

def last_completed_session():
    return trading_sessions(back_days=1, for_days=0)[0]

def next_n_sessions(n):
    return trading_sessions(back_days=0, for_days=n)

def str_as_dt(s):
    return datetime.strptime(s, "%Y-%m-%d")

def dt_as_str(dt):
    return dt.strftime("%Y-%m-%d")