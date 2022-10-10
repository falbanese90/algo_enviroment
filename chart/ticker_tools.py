from .alpaca_tools import api


def alpaca_active(exchange='None'):
    tick_list = []
    refined_list = []
    active_assets = api.list_assets(status='active')
    if exchange != 'None':
        active_assets = [n for n in active_assets if n.exchange == exchange.upper()]
    for n in active_assets:
        tick_list.append(n.symbol.split('/')[0])
    for n in tick_list:
        if len(n) < 5 and '.' not in n:
            refined_list.append(n)
    return refined_list
