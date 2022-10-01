import chart

if __name__ == '__main__':
    fail_count = 0
    t = chart.alpaca_active()
    for n in t:
        try:
            print(chart.Equity(n))
        except KeyError:
            print( f'{n}: Unable to load data')
            fail_count += 1
    print(f'Fails: {fail_count}\nOut of: {len(t)} requests')

    