from datetime import datetime
import psycopg2
from config import HOST, PORT, DATABASE
import csv
import pandas as pd
from .alpaca_tools import get_df
from tqdm import tqdm
from requests.exceptions import HTTPError
from .vol_premium import iv_prem
from .chart import weekdays
from datetime import datetime

## Establish Postgres Connection
conn = psycopg2.connect(host=HOST, port=PORT, database=DATABASE)
cur = conn.cursor()


def fetch_buys():
    ''' Returns query of all Buys in Database '''
    cur.execute("SELECT name FROM stocks WHERE buy='True'",)
    t = cur.fetchall()
    t = [n[0] for n in t]
    return t

def fetch_all(df=False):
    ''' Returns query of all items in Database '''
    cur.execute("SELECT * FROM stocks;")
    t = cur.fetchall()
    rows = []
    for n in t:
        row = [x for x in n]
        rows.append(row[1 ::])
    if df == True:
        df = pd.DataFrame(rows, columns=['Date', 'Name', 'Price', 'Buy', 'First_Test'])
        return df
    else:
        return rows

def export_csv(filename):
    ''' Exports Entire Database to CSV '''
    with open(f'{filename}.csv', 'w') as file:
        writer = csv.writer(file)
        for n in fetch_all():
            writer.writerow(n)
        return file

def first_test():
    ''' Screens current buy list for stocks 15% or more over the 5 year low. '''
    day = datetime.now().strftime('%A')
    if day not in weekdays:
        is_weekend = True
    else:
        is_weekend = False
    try:
        buys = fetch_buys()
        refined_buys = []
        for b in tqdm(buys):
            df = get_df(b, years_back=5, weekend=is_weekend)
            perc_over_low = ((df['close'][-1] - df['close'].min()) / df['close'].min()) * 100
            if perc_over_low >= 15 and float(df['close'][-1]) >= 5:
                refined_buys.append(b)
        refined_again = []
        for b in tqdm(refined_buys):
            vol = iv_prem(b)
            if vol['premium'] != str(None):
                if vol['premium'] >= 0:
                    refined_again.append(b)
        return refined_again

    except HTTPError as err:
        print(err)
        return refined_buys

        
