from .alpaca_tools import api


def alpaca_active(exchange='None'):
    ''' Returns a cleaned list of all active Alpaca Tickers '''
    active_assets = api.list_assets(status='active')
    if exchange != 'None':
        active_assets = [n for n in active_assets if n.exchange == exchange.upper()]
    active_assets = [n for n in active_assets if 'Acquisition' not in n.name or 'Receipts' not in n.name]
    tick_list = [n.symbol.split('/')[0] for n in active_assets]
    refined_list = [n for n in tick_list if len(n) < 5 or '.' not in n]
    return refined_list