from chart.db import conn, cur

if __name__ == '__main__':
    ''' Clears Database '''
    cur.execute('DROP TABLE stocks;')
    conn.commit()