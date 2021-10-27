import sqlite3
class generateResult:

    def genResult(election_id):
        conn = sqlite3.connect("ivote.db")
        c = conn.cursor()
        c.execute("select vote_given, count(*) from election"+str(election_id)+" group by vote_given")
        r = c.fetchall()
        for i in r:
            c.execute("insert into result('"+str(election_id)+",'"+str(r[0])+"'"+str(r[1])+")")

