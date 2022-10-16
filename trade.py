from chart.db import test_buys
from chart.trade import buy_bracket
from chart.model import Equity
import time
from chart.chart import day_of_the_week, weekdays
from tqdm import tqdm

def trade():
    if day_of_the_week in weekdays:
        buys = test_buys()
        for ticker in tqdm(buys):
            asset = Equity(ticker)
            buy_bracket(asset.name, asset.price)
            time.sleep(5)
    else:
        print('Its an off day..')
        time.sleep(5)

if __name__ == '__main__':   
        trade()



