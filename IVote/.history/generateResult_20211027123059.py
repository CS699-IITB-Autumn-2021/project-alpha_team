#importing the required library
import sqlite3


class generateResults:
    #function for generating the result
    def genResult(self,election_id):
        """ this is the fuction for generating the result of elections and 
        """
        #setting connection to the database (ivote.db)
        conn = sqlite3.connect("ivote.db")
        c = conn.cursor()
        c.execute("CREATE TABLE IF NOT EXISTS election"+str(election_id)+"(secret_code TEXT ,name_of_blockchain TEXT,voter_id TEXT,vote_given TEXT)")
        #executing the query for checking whether the election is active or not
        c.execute("select ended from election where electionid="+str(election_id))
        #fetching all the result 
        r = c.fetchall()
        # if election is active that means the result had not been calculated yet and return "result generated" message
        
        if(r[0][0]=='T') :
            #update the election and set election ended as F
            c.execute("update election set ended='F' where electionid="+str(election_id))
            #count all the votes of respective candidates
            c.execute("select vote_given, count(*) from election"+str(election_id)+" group by vote_given")
            
            
            r = c.fetchall()
            for i in r:
                c.execute("insert into result values('"+str(election_id)+"','"+str(r[0])+"',"+str(r[1])+")")
            conn.commit()
            conn.close()
            return "result generated"
        else :
            return "result already generated"
