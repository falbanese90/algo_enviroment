import csv
import os
from chart import model
import random
import pickle as pkl
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

def ticker_list(file):
    ORIGINAL_PATH = os.getcwd()
    os.chdir(ROOT_PATH + TICKER_PATH)
    tick_list = []
    with open(file) as f:
        reader = csv.reader(f)
        for row in reader:
            tick_list.append(row[0])
    return tick_list[1 ::]

def index(file):
    fail_count = 0
    t = ticker_list(file)
    random.shuffle(t)
    for n in t:
        try:
            print(model.Equity(n))
        except KeyError:
            print( f'{n}: Unable to load data')
            fail_count += 1
    print(f'Fails: {fail_count}\nOut of: {len(t)} requests')

def index_pkl(file):
    fail_count = 0
    os.chdir(ROOT_PATH + TICKER_PATH)
    with open(file, 'rb') as file:
        t = pkl.load(file)
    random.shuffle(t)
    for n in t:
        try:
            print(model.Equity(n))
        except KeyError:
            print( f'{n}: Unable to load data')
            fail_count += 1
    print(f'Fails: {fail_count}\nOut of: {len(t)} requests')

