import psycopg2
from config import HOST, PORT, DATABASE

conn = psycopg2.connect(host=HOST, port=PORT, database=DATABASE)
cur = conn.cursor()
