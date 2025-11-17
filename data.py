import sqlite3 as sql

dp=sql.connect('database.db')
cr=dp.cursor()
cr.execute('''CREATE TABLE IF NOT EXISTS users (username TEXT PRIMARY KEY, password TEXT NOT NULL, role TEXT NOT NULL)''')




