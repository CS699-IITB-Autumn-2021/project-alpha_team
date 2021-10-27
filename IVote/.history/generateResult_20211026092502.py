import sqlite3
class generateResult:

    def genResult(election_id):
        conn = sqlite3.connect("ivote.db")
        c = conn.cursor()