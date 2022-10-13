from chart.db import conn, cur

if __name__ == '__main__':
    cur.execute('DROP TABLE stocks;')
    conn.commit()