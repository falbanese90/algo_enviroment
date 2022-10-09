from http.client import RemoteDisconnected
from xmlrpc.client import ResponseError
import chart
import random
import traceback
import time
from chart.trade import buy
from chart.alpaca_tools import buying_power
import math

def run():
    x = 0
    fail_count = 0
    success_count = 0
    obj = {}
    errors_json = {}
    t = chart.alpaca_active(exchange='NASDAQ')
    random.shuffle(t)
    try:
        for n in t:
            try:
                obj_data = chart.Equity(n)
                print(obj_data)
                success_count += 1
                x += 1
                size = (obj_data.position_size * buying_power) / obj_data.price
                buy_qty = round(size, 0)
                if obj_data.is_buy == True:
                    buy(obj_data.name, buy_qty)
                if success_count % 1000 == 0:
                    time.sleep(120)
                elif success_count % 50 == 0:
                    time.sleep(60)
                
            except (KeyError, TypeError, AttributeError, ConnectionError, RemoteDisconnected) as error:
                print( f'{n}: Unable to load data')
                print(f'{error}\n')
                fail_count += 1
                errors_json[f'{n}'] = f'{traceback.extract_tb(error.__traceback__)}', f'{error}'
                ameritrade_ticker_fails = [n for n in errors_json.keys()]
            if fail_count > 0:
                print(f'Success: {success_count} / Fails: {fail_count}\nCapture Rate: {round(((success_count / (success_count + fail_count)) * 100), 3)}%')
            else:
                print(f'Success: {success_count} / Fails: {fail_count}\nCapture Rate: 100%')
    except (KeyboardInterrupt, ConnectionResetError, ResponseError):
        print('Updating Bad Ticker List before Executing')

    print(f'Fails: {fail_count}\nSuccess: {success_count}\nOut of: {len(t)} requests\nCapture Rate: {round(((success_count / (success_count + fail_count)) * 100), 3)}%')


if __name__ == '__main__':
    run()