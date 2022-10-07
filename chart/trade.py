from .alpaca_tools import api
from alpaca_trade_api.rest import APIError

def buy(ticker, amount):
    try:
        api.submit_order(
            symbol=ticker,
            qty=amount,
            side='buy',
            type='market',
            time_in_force='gtc'
        )
    except APIError as err:
        print(err)
        return

