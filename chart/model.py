from .chart import price, plot, market_cap
from .vol_premium import iv_prem as vol
from .toolbox import timer

from chart import vol_premium

class Equity():
    @timer
    def __init__(self, ticker):
        ''' Uses Data from API Requests to create Equity object '''
        self.name = str(ticker.upper())
        self.price = price(ticker.upper())['chart']['close'].iloc[-1]
        self.chart = price(ticker.upper())['chart']
        self.hist_vol = price(ticker.upper())['chart']['HV'][-1]

    def _plot(self, save_png=False):
        ''' Equity object Plot function '''
        plot(self.chart, self.name, save_png)

    def _export(self):
        ''' Exports Price DataFrame to CSV '''
        if self.chart == None:
            pass
        else:
            self.chart.to_csv(f'{self.name}.csv')

    @property
    def vol_prem(self):
        ''' Calculates Volatility Premium with Price and Options Data '''
        try:
            if vol(self.name.upper())['premium'] == None:
                return str(None)
            else:
                return vol(self.name.upper())['premium']
        except (KeyError, TypeError):
            return str(None)

    @property
    def intermediate_trend(self):
        ''' Checks if there is a intermediate trend in tact '''
        if self.chart['MA10'][-1] > self.chart['MA20'][-1]:
            return True
        else:
            return False

    @property
    def rsi_positive(self):
        ''' Checks if there is positive RSI conditions '''
        if 40 <= self.chart['RSI'][-1] <= 60:
            return True
        else:
            return False

    @property
    def macd_positive(self):
        ''' Checks MACD signal '''
        if self.chart['MACD'][-1] > 0:
            return True
        else:
            return False

    @property
    def volume_positive(self):
        ''' Checks if there is More than 20Day Average in Volume '''
        if self.chart['volume'][-1] > self.chart['Volume20MA'][-1]:
            return True
        else:
            return False

    @property
    def bollinger_positive(self):
        ''' Checks to see if price is under the middle Bollinger Band '''
        if self.price <= self.chart['bollinger'][-1]:
            return True
        else:
            return False

    @property
    def is_buy(self):
        ''' Checks if to see if it meets the Buy Requirement: Four of Five Conditions Met '''
        counter = 0
        if self.intermediate_trend:
            counter += 1
        if self.rsi_positive:
            counter += 1
        if self.macd_positive:
            counter += 1
        if self.volume_positive:
            counter += 1
        if self.bollinger_positive:
            counter += 1
        if counter == 4:
            return True
        else:
            return False

    
    @property
    def iv(self):
        ''' Gets Implied Vol if Exists '''
        try:
            if vol(self.name.upper())['implied_vol'] == None:
                return str(None)
            else:
                return vol(self.name.upper())['implied_vol']
        except (KeyError, TypeError):
            return str(None)

    @property
    def MC(self):
        ''' Gets Market Cap if Known '''
        try:
            mc = market_cap(self.name)
            if mc != None:
                if mc >= 10000000000:
                    return 'Large'
                elif 2000000000 <= mc < 10000000000:
                    return 'Mid'
                elif 300000000 <= mc < 2000000000:
                    return 'Small'
                else:
                    return 'Micro'
            else:
                return 'Unknown'
        except (IndexError, KeyError):
            return 'Unknown'

    @property
    def position_size(self):
        ''' Attempts to find position Size according to market cap '''
        if self.MC != 'Unknown':
            return .04
        else:
            if self.MC == 'Large':
                return .12
            elif self.MC == 'Mid':
                return .09
            elif self.MC == 'Small':
                return .06
            else:
                return .05


    def __str__(self):
        ''' Returns String Representation of Object '''
        return (f'{self.name}: {self.price}\n'
               f'Historical Vol: {self.hist_vol}\n'
               f'Implied Vol: {self.iv}\n'
               f'Vol Premium: {self.vol_prem}\nBuy: {self.is_buy}\nMarket Cap: {self.MC}\nPosition Size: {self.position_size * 100}%\n')



