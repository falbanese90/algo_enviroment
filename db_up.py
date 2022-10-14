from chart.db import conn, cur
import time

if __name__ == '__main__':
    ''' Creates Database Structure '''

    cur.execute(
        'CREATE TABLE stocks(id SERIAL PRIMARY KEY, date VARCHAR NOT NULL, name VARCHAR NOT NULL, price float NOT NULL, buy VARCHAR NOT NULL, first_test VARCHAR);'
        )
    
    conn.commit()
    print('Database Ready..')
    time.sleep(2)