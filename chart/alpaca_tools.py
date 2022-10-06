import alpaca_trade_api as alpaca
from config import ALPACA_KEY, ALPACA_SECRET, ALPACA_URL
from alpaca_trade_api.rest import TimeFrame
import datetime
from dateutil.relativedelta import relativedelta
import pandas as pd

api = alpaca.REST(ALPACA_KEY, ALPACA_SECRET, ALPACA_URL)
last_year = (datetime.datetime.now() - relativedelta(years=1)).strftime('%Y-%m-%d')
yesterday = (datetime.datetime.now() - relativedelta(days=1)).strftime('%Y-%m-%d')

def get_df(ticker):
    df = api.get_bars(ticker, TimeFrame.Day, last_year, yesterday, adjustment='raw').df
    df['datetime'] = pd.to_datetime(df.index, unit='ms').strftime('%m/%d/%Y')
    return df

