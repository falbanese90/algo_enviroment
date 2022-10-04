from http.client import RemoteDisconnected
import requests
import pandas as pd
import time
import matplotlib.pyplot as plt
from config import ameritrade
import math
import numpy as np



def price(ticker):
    try:
        try:
            ticker = ticker.upper()
            result = requests.get('https://api.tdameritrade.com/v1/instruments',
                                params={'apikey': ameritrade, 'symbol': ticker,
                                'projection': 'fundamental'})
        except (ConnectionResetError, RemoteDisconnected):
            print('Connection Resetting, 10 seconds')
            time.sleep(10)
            ticker = ticker.upper()
            result = requests.get('https://api.tdameritrade.com/v1/instruments',
                                params={'apikey': ameritrade, 'symbol': ticker,
                                'projection': 'fundamental'})
        data = result.json()
        fd = data[ticker]['fundamental'] if 'fundamental' in data[ticker] else None

        result  = requests.get(f'https://api.tdameritrade.com/v1/marketdata/{ticker}/pricehistory', 
                            params={'apikey': ameritrade, 'periodType': 'year', 'frequencyType': 'daily'})
        data = result.json()
        df = get_chart(data)
        dict = {'chart': df, 'fundamental': fd}
        return dict
    except KeyError:
        pass


def plot(dataframe, title, save_png=False):
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
    try:
        ticker = ticker.upper()
        result = requests.get('https://api.tdameritrade.com/v1/marketdata/chains',
                            params={'apikey': ameritrade, 'symbol': ticker,
                            'contractType': 'CALL', 'strategy': 'ANALYTICAL', 'strikeCount': '1'})
    except (ConnectionResetError, RemoteDisconnected):
        print('Connection Resetting, 10 seconds')
        time.sleep(10)
        ticker = ticker.upper()
        result = requests.get('https://api.tdameritrade.com/v1/marketdata/chains',
                            params={'apikey': ameritrade, 'symbol': ticker,
                            'contractType': 'CALL', 'strategy': 'ANALYTICAL', 'strikeCount': '1'})
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
    for n in data_request_json['candles']:
        n['datetime'] = pd.to_datetime(n['datetime'], unit='ms').strftime('%m/%d/%Y')

    candles = data_request_json['candles']
    df = pd.DataFrame.from_dict(candles)
    df = df.iloc[:, ::-1]
    df['MA10'] = df['close'].rolling(window=10).mean()
    df['MA20'] = df['close'].rolling(window=20).mean()
    df['MA50'] = df['close'].rolling(window=50).mean()
    df['MA100'] = df['close'].rolling(window=100).mean()
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