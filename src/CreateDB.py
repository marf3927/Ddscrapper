import sqlite3

conn = sqlite3.connect("../dogDrip.db")
cur = conn.cursor()
cur.execute("CREATE TABLE IF NOT EXISTS dogDrip(id integer PRIMARY KEY, title TEXT, address TEXT, HTTP TEXT)")
