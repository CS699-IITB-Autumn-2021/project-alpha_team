import sqlite3


conn = sqlite3.connect("ivote.db")
c = conn.cursor()
c.execute("insert into result values('2','1',12)")


conn.commit()
conn.close()