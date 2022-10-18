from .alpaca_tools import api
from alpaca_trade_api.rest import APIError

account = api.get_account()
large_pos = (.12 * float(account.buying_power))
mid_position = (.09 * float(account.buying_power))
small_position = (.06 * float(account.buying_power))
default_position = (.05 * float(account.buying_power))

def position_qty(price, size=default_position):
    q = round((size / price), 0)
    return q


def buy_bracket(ticker, price, size=None):
    ''' Submits Buy order '''
    try:
        api.submit_order(
            symbol=ticker,
            qty=position_qty(price),
            side='buy',
            type='market',
            time_in_force='gtc',
            order_class='bracket',
            take_profit=dict(
                limit_price = round(price + (.15 * price), 2)
            ),
            stop_loss=dict(
                stop_price = round(price - (price * .05), 2),
                limit_price = round(price - (price * .05), 2)
            )
        )
    except APIError as err:
        print(err)
        return

