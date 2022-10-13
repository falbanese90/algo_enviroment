from asyncore import write
import chart
import random
import traceback
import time
import csv
from chart.db import cur, conn

def run():
    rows = []
    x = 0
    success_count = 0
    t = chart.alpaca_active(exchange='NASDAQ')
    random.shuffle(t)
    try:
        for n in t:
            try:
                time.sleep(.5)
                obj_data = chart.Equity(n)
                print(obj_data)
                success_count += 1
                print(f'Succeses: {success_count}')
                x += 1
                rows.append([obj_data.name, obj_data.price, obj_data.chart['MA10'][-1], obj_data.chart['MA20'][-1], obj_data.chart['Volume20MA'][-1], obj_data.chart['RSI'][-1], obj_data.chart['MACD'][-1], obj_data.chart['HV'][-1], obj_data.is_buy])
                cur.execute('INSERT INTO stocks (date, name, price, buy) VALUES (%s, %s, %s, %s)', (str(obj_data.chart.index[-1]), str(obj_data.name), float(obj_data.price), str(obj_data.is_buy)))
                conn.commit()
                if success_count % 1000 == 0:
                    time.sleep(240)
                elif success_count % 50 == 0:
                    time.sleep(30)
            except Exception:
                pass
                
    except Exception:
        with open('error.txt', 'w') as file:
            file.write(f'{traceback.format_exc()}')

    with open('scan.csv', 'w') as file:
        writer = csv.writer(file)
        for n in rows:
            writer.writerow(n)


if __name__ == '__main__':
    run()