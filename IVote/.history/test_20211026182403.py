import sqlite3


conn = sqlite3.connect("ivote.db")
c = conn.cursor()
c.execute("insert into admin values('admin@gmail.com','admin')")