from chart.db import conn, cur
import time

if __name__ == '__main__':
    ''' Clears Database '''
    answer = input('You are about to clear the database completely. Are you sure?\ny: Yes\n')
    if answer == 'y':
        print('Tearing down Database..')
        cur.execute('DROP TABLE stocks;')
        conn.commit()
        print('Complete')
    else:
        print('Aborting Tear Down..')
        time.sleep(2)