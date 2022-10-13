from unicodedata import name
import psycopg2
from config import HOST, PORT, DATABASE
import csv
import pandas as pd

## Establish Postgres Connection
conn = psycopg2.connect(host=HOST, port=PORT, database=DATABASE)
cur = conn.cursor()

def fetch_buys():
    ''' Returns query of all Buys in Database '''
    cur.execute("SELECT name FROM stocks WHERE buy='True';")
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
        df = pd.DataFrame(rows, columns=['Date', 'Name', 'Price', 'Buy'])
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

        
