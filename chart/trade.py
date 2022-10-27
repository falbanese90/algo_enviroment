from .alpaca_tools import api
from alpaca_trade_api.rest import APIError
import chart.db as db
import time

## Create Scales of Position sizing frames
large_pos = (.12 * float(90000))
mid_position = (.09 * float(90000))
small_position = (.06 * float(90000))
default_position = (.05 * float(90000))

## Call api for a list of current positions
positions = [n.symbol for n in api.list_positions()]

def position_qty(price, size=default_position):
    q = round((size / price), 0)
    return q

def buy_bracket(ticker, price, stop, size=None):
    ''' Submits Buy order '''
    try:
        api.submit_order(
            symbol=ticker,
            qty=position_qty(price),
            side='buy',
            type='market',
            time_in_force='gtc',
        )
        time.sleep(1)
        api.submit_order(
            symbol=ticker,
            qty=position_qty(price),
            side='sell',
            type='trailing_stop',
            time_in_force='gtc',
            trail_percent=stop
        )

    except APIError as err:
        print(err)
        return

def close_position(symbol, qty):
    try:
        api.submit_order(
            symbol=symbol,
            qty=qty,
            side='sell',
            type='market',
            time_in_force='gtc',
        )
    except APIError as err:
        print(err)
        return

def close_nulled_buys():
    buys = db.fetch_buys()
    positions_symbols = [n.symbol for n in api.list_positions()]
    not_buy = lambda x: x not in buys
    closeout = []
    close_filter = filter(not_buy, positions_symbols)
    for n in close_filter:
        closeout.append(n)
    orders = api.list_orders(symbols=closeout)
    for n in orders:
        api.cancel_order(n.id)
    for n in positions_symbols:
        qty = api.get_position(n).qty
        close_position(n, qty)


    