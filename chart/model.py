from ast import And, expr_context
from operator import truediv
from .chart import price, plot
from .vol_premium import iv_prem as vol
from .toolbox import timer
import pandas as pd

from chart import vol_premium

class Equity():
    @timer
    def __init__(self, ticker):
        self.name = price(ticker.upper())['fundamental']['symbol']
        self.fundamental = price(ticker.upper())['fundamental']
        self.price = price(ticker.upper())['chart']['close'].iloc[-1]
        self.chart = price(ticker.upper())['chart']
        self.hist_vol = vol(ticker.upper())['historical_vol']
        self.peg = price(ticker.upper())['fundamental']['pegRatio']


    def _plot(self, save_png=False):
        if self.chart == None:
            pass
        else:     
            plot(self.chart, self.name, save_png)

    def _export(self):
        if self.chart == None:
            pass
        else:
            self.chart.to_csv(f'{self.name}.csv')

    @property
    def vol_prem(self):
        try:
            if vol(self.name.upper())['premium'] == None:
                return str(None)
            else:
                return vol(self.name.upper())['premium']
        except KeyError:
            return str(None)

    @property
    def is_buy(self):
        if self.chart['MA10'][-1] > self.chart['MA20'][-1]:
            return True
        else:
            return False
    
    @property
    def iv(self):
        try:
            if vol(self.name.upper())['implied_vol'] == None:
                return str(None)
            else:
                return vol(self.name.upper())['implied_vol']
        except KeyError:
            return str(None)

    def __str__(self):
        return (f'{self.name}: {self.price}\n'
               f'Historical Vol: {self.hist_vol}\n'
               f'Implied Vol: {self.iv}\n'
               f'Vol Premium: {self.vol_prem}\nBuy: {self.is_buy}\n')



