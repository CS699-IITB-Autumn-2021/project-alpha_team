import sqlite3

#this is for testing purpose
conn = sqlite3.connect("ivote.db")
c = conn.cursor()
c.execute("insert into result values('2','1',12)")


conn.commit()
conn.close()