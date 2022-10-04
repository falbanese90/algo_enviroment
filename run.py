import chart
import json
import random
import traceback
import pickle as pkl

def ticker_run():
    fail_count = 0
    success_count = 0
    obj = {}
    errors_json = {}
    t = chart.alpaca_active()
    random.shuffle(t)

    for n in t:
        with open('ameritrade_ticker_fails.pkl', 'rb') as file:
            bad_ticker = pkl.load(file)
        if n in bad_ticker:
            pass
        else:
            try:
                obj_data = chart.Equity(n)
                print(obj_data)
                success_count += 1
            except (KeyError, TypeError, AttributeError, ConnectionError) as error:
                print( f'{n}: Unable to load data')
                print(f'{error}\n')
                fail_count += 1
                errors_json[f'{n}'] = f'{traceback.extract_tb(error.__traceback__)}', f'{error}'
                ameritrade_ticker_fails = [n for n in errors_json.keys()]
                with open('ameritrade_ticker_fails.pkl', 'wb') as file:
                    bad_ticker.append(ameritrade_ticker_fails)
                    pkl.dump(bad_ticker, file)
            if fail_count > 0:
                print(f'Success: {success_count} / Fails: {fail_count}\nCapture Rate: {round(((success_count / fail_count) * 100), 3)}%')
            else:
                print(f'Success: {success_count} / Fails: {fail_count}\nCapture Rate: 100%')

    print(f'Fails: {fail_count}\nSuccess: {success_count}\nOut of: {len(t)} requests\nCapture Rate: {round(((success_count / fail_count) * 100), 3)}%')
    with open('errors.json', 'w') as file:
        json.dump(errors_json, file, indent=4)

if __name__ == '__main__':
    ticker_run()


