from .alpaca_tools import api
from alpaca_trade_api.rest import APIError

def buy(ticker, amount):
    ''' Submits Buy order '''
    try:
        api.submit_order(
            symbol=ticker,
            qty=amount,
            side='buy',
            type='market',
            time_in_force='day'
            )
    except APIError as err:
        print(err)
        return

