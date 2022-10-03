import chart
import json
import random
import traceback


if __name__ == '__main__':
    fail_count = 0
    success_count = 0
    obj = {}
    errors_json = {}
    t = chart.alpaca_active()
    random.shuffle(t)
    # with open('errors.json', 'r') as file:
    #     t = json.load(file)
    # t = t.keys()
    for n in t:
        try:
            obj_data = chart.Equity(n)
            print(obj_data)
            success_count += 1
        except (KeyError, TypeError, AttributeError) as error:
            print( f'{n}: Unable to load data')
            print(f'{error}\n')
            fail_count += 1
            errors_json[f'{n}'] = f'{traceback.extract_tb(error.__traceback__)}', f'{error}'
        print(f'Success: {success_count} / Fails: {fail_count}')
    print(f'Fails: {fail_count}\nSuccess: {success_count}\nOut of: {len(t)} requests\nCapture Rate: {success_count / fail_count}')
    with open('errors.json', 'w') as file:
        json.dump(errors_json, file, indent=4)


