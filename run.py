from asyncore import write
from http.client import RemoteDisconnected
from xmlrpc.client import ResponseError
import chart
import random
import traceback
import time
from chart.trade import buy
from chart.alpaca_tools import buying_power
from chart.send_msg import send_error
import csv

def run():
    rows = []
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
                time.sleep(.5)
                obj_data = chart.Equity(n)
                print(obj_data)
                success_count += 1
                x += 1
                rows.append([obj_data.name, obj_data.price, obj_data.chart['MA10'][-1], obj_data.chart['MA20'][-1], obj_data.chart['Volume20MA'][-1], obj_data.chart['RSI'][-1], obj_data.chart['MACD'][-1], obj_data.chart['HV'][-1], obj_data.is_buy])
                # size = (obj_data.position_size * buying_power) / obj_data.price
                # buy_qty = int(round(size, 0))
                # if obj_data.is_buy == True:
                #     buy(obj_data.name, buy_qty)
                if success_count % 1000 == 0:
                    time.sleep(240)
                elif success_count % 50 == 0:
                    time.sleep(30)
                
            except (KeyError, TypeError, AttributeError, ConnectionError, RemoteDisconnected) as error:
                print( f'{n}: Unable to load data')
                print(f'{error}\n')
                send_error(error)
                with open('scan.csv', 'w') as file:
                    writer = csv.writer(file)
                    for n in rows:
                        writer.writerow(n)
            if fail_count > 0:
                print(f'Success: {success_count} / Fails: {fail_count}\nCapture Rate: {round(((success_count / (success_count + fail_count)) * 100), 3)}%')
            else:
                print(f'Success: {success_count} / Fails: {fail_count}\nCapture Rate: 100%')
    except (KeyboardInterrupt, ConnectionResetError, ResponseError):
        print('Updating Bad Ticker List before Executing')

    print(f'Fails: {fail_count}\nSuccess: {success_count}\nOut of: {len(t)} requests\nCapture Rate: {round(((success_count / (success_count + fail_count)) * 100), 3)}%')
    with open('scan.csv', 'w') as file:
        writer = csv.writer(file)
        for n in rows:
            writer.writerow(n)


if __name__ == '__main__':
    run()