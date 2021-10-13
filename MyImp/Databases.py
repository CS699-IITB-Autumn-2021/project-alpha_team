import sqlite3






#for creating all the tables in database
class iVote():
    def __init__(self):
        self.con = sqlite3.connect("iVote.db")
        self.cur = self.con.cursor()  
        self.cur.execute(""" CREATE TABLE IF NOT EXISTS User_Info(Name text , email text ,id_number text , user_password text)""")
        #admin info should be entered manually
        self.cur.execute(""" CREATE TABLE IF NOT EXISTS Admin_Info(Name text , email text ,id_number text , user_password text)""")
        self.cur.execute(""" CREATE TABLE IF NOT EXISTS Elections(Ele_Name text , Desc_of_ele text ,election_id text , user_password text,start_date date, end_date date , no_of_candidates integer ,PRIMARY KEY (election_id))""")
        self.con.commit()

    def createTableForEachElection(self,election_id):
        self.con = sqlite3.connect("iVote.db")
        self.cur = self.con.cursor()  
        self.cur.execute(" CREATE TABLE IF NOT EXISTS election_"+election_id+"(election_id text, candidate_id_number text , votes integer ,)")
        self.con.commit()

    def print_all_data_ForEachElection(self,election_id):
        self.cur.execute("SELECT * FROM employeeInfo")
        records = self.cur.fetchall()
        print("Name\tID\tSalary\tCity")
        for row in records :
            print(row[0]+"\t"+str(row[1])+"\t"+str(row[2])+"\t"+row[3],end="")
        
        
v= iVote()
