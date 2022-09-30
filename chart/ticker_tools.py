import csv

def ticker_list(file):
    tick_list = []
    with open(file) as f:
        reader = csv.reader(f)
        for row in reader:
            tick_list.append[row[0]]
    return tick_list        
