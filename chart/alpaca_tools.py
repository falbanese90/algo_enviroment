import alpaca_trade_api as alpaca
from config import ALPACA_KEY, ALPACA_SECRET, ALPACA_URL
from alpaca_trade_api.rest import TimeFrame
import datetime
from dateutil.relativedelta import relativedelta
import pandas as pd
import time

## ALPACA API Configuration
api = alpaca.REST(ALPACA_KEY, ALPACA_SECRET, ALPACA_URL)

yesterday = (datetime.datetime.now() - relativedelta(days=1)).strftime('%Y-%m-%d')
account = api.get_account()
buying_power = float(account.buying_power)

def get_df(ticker, years_back=1, weekend=False):
    ''' Retrieves price data from alpaca API '''
    time.sleep(.5)
    if weekend:
        if datetime.datetime.now().strftime('%A') == 'Saturday':
            yesterday = (datetime.datetime.now() - relativedelta(days=1)).strftime('%Y-%m-%d')
        elif datetime.datetime.now().strftime('%A') == 'Sunday':
            yesterday = (datetime.datetime.now() - relativedelta(days=2)).strftime('%Y-%m-%d')
        last_year = (
        datetime.datetime.now() - relativedelta(
            years=years_back
            )
        ).strftime('%Y-%m-%d')
        df = api.get_bars(
            ticker, TimeFrame.Day, 
            last_year, yesterday, 
            adjustment='raw'
            ).df
        df['datetime'] = pd.to_datetime(
            df.index, 
            unit='ms'
            ).strftime('%m/%d/%Y')
        return df
    else:
        yesterday = (datetime.datetime.now() - relativedelta(days=1)).strftime('%Y-%m-%d')
        last_year = (
            datetime.datetime.now() - relativedelta(
                years=years_back
                )
            ).strftime('%Y-%m-%d')
        df = api.get_bars(
            ticker, TimeFrame.Day, 
            last_year, yesterday, 
            adjustment='raw'
            ).df
        df['datetime'] = pd.to_datetime(
            df.index, 
            unit='ms'
            ).strftime('%m/%d/%Y')
        return df

def get_df_months(ticker, months_back=2):
    time.sleep(.5)
    last_year = (
        datetime.datetime.now() - relativedelta(
            months=months_back
            )
        ).strftime('%Y-%m-%d')
    df = api.get_bars(
        ticker, TimeFrame.Day, 
        last_year, yesterday, 
        adjustment='raw'
        ).df
    df['datetime'] = pd.to_datetime(
        df.index, 
        unit='ms'
        ).strftime('%m/%d/%Y')
    return df

def alpaca_active(exchange='None'):
    ''' Returns a cleaned list of all active Alpaca Tickers '''
    active_assets = api.list_assets(status='active')
    if exchange != 'None':
        active_assets = [n for n in active_assets if n.exchange == exchange.upper()]
    active_assets = [n for n in active_assets if 'Acquisition' not in n.name or 'Receipts' not in n.name or 'Shares' not in n.name or 'Fund' not in n.name or 'ETF' not in n.name]
    tick_list = [n.symbol.split('/')[0] for n in active_assets]
    refined_list = [n for n in tick_list if len(n) < 5 or '.' not in n]
    return refined_list


