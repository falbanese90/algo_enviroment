from .chart import price, plot
from .vol_premium import iv_prem as vol
from .toolbox import timer

from chart import vol_premium

class Equity():
    @timer
    def __init__(self, ticker):
        self.name = str(ticker.upper())
        self.price = price(ticker.upper())['chart']['close'].iloc[-1]
        self.chart = price(ticker.upper())['chart']
        self.hist_vol = price(ticker.upper())['chart']['HV'][-1]

    def _plot(self, save_png=False):
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
        except (KeyError, TypeError):
            return str(None)

    @property
    def intermediate_trend(self):
        if self.chart['MA10'][-1] > self.chart['MA20'][-1]:
            return True
        else:
            return False

    @property
    def rsi_positive(self):
        if 40 <= self.chart['RSI'][-1] <= 60:
            return True
        else:
            return False

    @property
    def macd_positive(self):
        if self.chart['MACD'][-1] > 0:
            return True
        else:
            return False

    @property
    def volume_positive(self):
        if self.chart['volume'][-1] > self.chart['Volume20MA'][-1]:
            return True
        else:
            return False

    @property
    def is_buy(self):
        counter = 0
        if self.intermediate_trend:
            counter += 1
        if self.rsi_positive:
            counter += 1
        if self.macd_positive:
            counter += 1
        if self.volume_positive:
            counter += 1
        if counter == 4:
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
        except (KeyError, TypeError):
            return str(None)

    def __str__(self):
        return (f'{self.name}: {self.price}\n'
               f'Historical Vol: {self.hist_vol}\n'
               f'Implied Vol: {self.iv}\n'
               f'Vol Premium: {self.vol_prem}\nBuy: {self.is_buy}\n')



