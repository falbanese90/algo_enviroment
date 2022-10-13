import requests
import pandas as pd
import time
import matplotlib.pyplot as plt
from config import ameritrade
import math
import numpy as np
from .alpaca_tools import get_df
from requests.exceptions import ConnectionError
from stockstats import wrap
from pandas_datareader import data
from requests.exceptions import ConnectionError


def price(ticker):
    ''' 
    Uses Alpaca to recieve price data in order to return
    a dictionary object with DataFrame and Fundamental
    JSON. The Fundamental data has been removed for now.
    '''
    df = get_df(ticker)
    try:
        df = add_ta(df)
    except (KeyError, TypeError):
        return
    fd = None
    dict = {'chart': df, 'fundamental': fd}
    return dict


def plot(dataframe, title, save_png=False):
    ''' Plots the DataFrame to a PNG '''
    plt.figure(figsize=[16, 8])
    plt.plot(dataframe['close'], label=title)
    plt.plot(dataframe['MA10'], label='MA10')
    plt.plot(dataframe['MA20'], label='MA20')
    plt.ylabel('Price')
    plt.xlabel('Date')
    plt.legend()
    if save_png == True:
        plt.savefig(f'{title}.png')
    else:
        pass
    ax = plt.gca()
    ax.axes.xaxis.set_ticks([])
    plt.grid(True)
    plt.show()


def options(ticker):
    ''' 
    Attempts to recieve Options Data from Ameritrade API
    If successful returns the most recent monthly Implied Vol
    '''
    try:
        ticker = ticker.upper()
        result = requests.get(
            'https://api.tdameritrade.com/v1/marketdata/chains',
                            params={
                                'apikey': ameritrade, 
                                'symbol': ticker,
                                'contractType': 'CALL', 
                                'strategy': 'ANALYTICAL', 
                                'strikeCount': '1'
                                })
    except ConnectionError as error:
        print(error)
        time.sleep(30)
        ticker = ticker.upper()
        result = requests.get(
            'https://api.tdameritrade.com/v1/marketdata/chains',
                            params={
                                'apikey': ameritrade, 
                                'symbol': ticker,
                                'contractType': 'CALL', 
                                'strategy': 'ANALYTICAL', 
                                'strikeCount': '1'
                                })
    data = result.json()
    exp = [n for n in data['callExpDateMap'].keys()]
    strike = {}
    if len(exp) < 5:
        return None
    else:     
        strike[f'{exp[4]}'] = data['callExpDateMap'][exp[4]]
        x = 0
        while x <= 1:
            for n in strike.keys():
                key = n
            strike = strike[key]
            x += 1
        return strike[0]

def get_chart(data_request_json):
    ''' Parses data into Dataframe from Ameritrade price request '''
    for n in data_request_json['candles']:
        n['datetime'] = pd.to_datetime(
            n['datetime'], 
            unit='ms').strftime('%m/%d/%Y'
            )

    candles = data_request_json['candles']
    df = pd.DataFrame.from_dict(candles)
    df = add_ta(df)
    return df

def add_ta(df):
    ''' Adds additional Technical Analysis to Raw DataFrame '''
    df = df.iloc[:, ::-1]
    stats = wrap(df)
    df['MA10'] = df['close'].rolling(window=10).mean()
    df['MA20'] = df['close'].rolling(window=20).mean()
    df['MA50'] = df['close'].rolling(window=50).mean()
    df['MA100'] = df['close'].rolling(window=100).mean()
    df['Volume20MA'] = df['volume'].rolling(window=20).mean()
    df['RSI'] = stats['rsi']
    df['MACD'] = stats['macdh']
    df['bollinger'] = stats['boll']
    x = 0
    l = []
    for n in df['close']:
        if x == 0:
            n = None
        else:
            n = np.log(n / df['close'][x - 1])
        x += 1
        l.append(n)
    df['Log returns'] = l
    
    df['HVSD30'] = df['Log returns'].rolling(30).std()
    list = []
    for n in df['HVSD30']:
        if n is None:
            result = None
        else:
            result = round((n * math.sqrt(252)) * 100, 3)
        list.append(result)
    df['HV'] = list
    df.set_index('datetime', inplace=True)
    return df

def market_cap(ticker):
    ''' Attempts to Find Market Cap from Yahoo data '''
    try:
        market_cap = data.get_quote_yahoo(ticker.upper())['marketCap']
        return market_cap[-1]
    except Exception:
        return None
