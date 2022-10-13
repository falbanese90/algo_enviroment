from chart.db import conn, cur

if __name__ == '__main__':
    ''' Creates Database Structure '''
    cur.execute('CREATE TABLE stocks(id SERIAL PRIMARY KEY, date VARCHAR, name VARCHAR, price float, buy VARCHAR);')
    conn.commit()
