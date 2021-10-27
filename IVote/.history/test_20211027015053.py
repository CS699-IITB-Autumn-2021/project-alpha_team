import sqlite3


conn = sqlite3.connect("ivote.db")
c = conn.cursor()
c.execute("insert into result values('1','1',12)")
c.execute("insert into result values('1','2',12)")
c.execute("insert into result values('1','3',12)")
c.execute("insert into result values('1','4',12)")
c.execute("insert into result values('1','4',12)")

conn.commit()
conn.close()