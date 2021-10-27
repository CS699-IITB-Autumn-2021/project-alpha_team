import sqlite3

#this is for testing purpose
conn = sqlite3.connect("ivote.db")
c = conn.cursor()
c.execute("insert into admin values('admin@gmail.com','admin')")


conn.commit()
conn.close()