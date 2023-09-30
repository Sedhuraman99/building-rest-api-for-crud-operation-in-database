import pymysql
from pymysql.cursors import DictCursor

conn = pymysql.connect(
    host="sql12.freesqldatabase.com",
    database="sql12649901",
    user="sql12649901",
    password="6Nxz6zhI4K",
    port=3306,
    charset="utf8mb4",
    cursorclass=pymysql.cursors.DictCursor
)

cursor = conn.cursor()
sql_query = """ CREATE TABLE Products (
    id integer PRIMARY KEY,
    name text NOT NULL,
    barcode text NOT NULL,
    brand text NOT NULL,
    description text NOT NULL,
    price text NOT NULL,
    available text NOT NULL
)"""
cursor.execute(sql_query)
conn.close()

