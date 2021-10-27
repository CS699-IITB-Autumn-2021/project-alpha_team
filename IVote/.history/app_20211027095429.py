from posixpath import lexists
import re
import sqlite3
import random
import os.path
from flask import Flask, render_template, request,redirect,session
from flask.helpers import url_for
from datetime import date
from datetime import datetime
from pathlib import Path
from werkzeug.utils import redirect
from generateResult import generateResults
from blockchainImp import Block



app = Flask(__name__)
app.secret_key="ivote"

conn = sqlite3.connect("ivote.db")
c = conn.cursor()
"""creating all the required tables 
"""
c.execute("CREATE TABLE IF NOT EXISTS Voters(name TEXT,email TEXT,cardno TEXT,password TEXT,voted TEXT)")
c.execute("CREATE TABLE IF NOT EXISTS admin(email TEXT,password TEXT)")
c.execute("CREATE TABLE IF NOT EXISTS election(electionid INTEGER,topic TEXT,startdate TEXT,enddate TEXT,numcand INTEGER,ended Text)")
c.execute("CREATE TABLE IF NOT EXISTS candidate(name TEXT,electionid INTEGER,candidateid TEXT,age INTEGER,mobno INTEGER,email TEXT)")
c.execute("CREATE TABLE IF NOT EXISTS result(election_id Text,cand_id Text, noofvotes Number)")
c.execute("SELECT electionid FROM election")
r = c.fetchall()
for i in r:
    fle = Path("static/blockchain/"+str(i[0])+".txt")
    c.execute("CREATE TABLE IF NOT EXISTS election"+str(i[0])+"(secret_code TEXT ,name_of_blockchain TEXT,voter_id TEXT,vote_given TEXT)")
    fle.touch(exist_ok=True)
    f = open(fle)

conn.commit()
conn.close()

@app.route('/',methods=['GET','POST'])
def login():
    """ This view takes request for login from the Voter and if the credentials are found valid according to database
        
        then will allowed to go further in the portal.
        
        Otherwise the voter will be stopped here to put valid credentials.
    """
    r = ""
    if request.method=="POST":
        email = request.form["email"]
        password = request.form["password"]
        conn = sqlite3.connect("ivote.db")
        c = conn.cursor()
        c.execute("SELECT * FROM Voters WHERE email='"+email+"' and password='"+password+"'")
        r = c.fetchall()
        for i in r:
            if email==i[1] and password == i[3]:
                session["voter"] = i[0]
                session["voterid"] = i[2]
                return redirect(url_for("voter"))
    return render_template('home.html')


@app.route('/signup.html',methods=['GET','POST'])
def signup():
    """ This view will take an request for Signup for voters.
    """
    if request.method=="POST":
        name = request.form["name"]
        email = request.form["email"]
        cardno = request.form["id"]
        password = request.form["password"]
        confirm = request.form["confirm"]
        if password==confirm:
            conn = sqlite3.connect("ivote.db")
            c = conn.cursor()
            c.execute("INSERT INTO Voters VALUES('"+name+"','"+email+"','"+cardno+"','"+password+"','True')")
            conn.commit()
            conn.close()
            return  render_template('login.html')
    return  render_template('signup.html')

@app.route('/Login.html',methods=['GET','POST'])
def adminlogin():
    """ This view takes request for login from the Admin and if the credentials are found valid according to database
        
        then will allowed to go further in the portal.
        
        Otherwise the Admin will be stopped here to put valid credentials.
    """
    r = ""
    if request.method=="POST":
        email = request.form["email"]
        password = request.form["password"]
        conn = sqlite3.connect("ivote.db")
        c = conn.cursor()
        c.execute("SELECT * FROM admin WHERE email='"+email+"' and password='"+password+"'")
        r = c.fetchall()
        for i in r:
            if email==i[0] and password == i[1]:
                session["admin"]=True
                session["email"]=email
                return redirect(url_for("admin")) 
    return  render_template('Login.html')


@app.route('/forgotPassword.html',methods=['GET','POST'])
def forgot():
    """ This view is to provide the facility of password reset if the voter or admin wants to reset their password.
    """
    
    if request.method=="POST":
        
        return  render_template('login.html')
    return  render_template('forgotPassword.html')

    


@app.route('/admin.html',methods = ['GET','POST'])
def admin():
    """ Home page for admin after login. This view takes a request for creation of election with an unique id.
    """
    if "admin" in session:
        msg = None
        if request.method=="POST":
            id = request.form['id']
            topic = request.form['topic']
            start = request.form['startdate']
            end = request.form['enddate']
            numcand = request.form['numcand']
            conn = sqlite3.connect("ivote.db")
            c = conn.cursor()
            c.execute("SELECT * from election WHERE electionid = '"+id+"'")
            r = c.fetchall()
            if len(r)>=1:
                msg = "Election with this id already exist"
            else :
                c.execute("INSERT INTO election VALUES('"+id+"','"+topic+"','"+start+"','"+end+"','"+numcand+"','T')")
                conn.commit()
                conn.close()
                msg = "Election created"
        return render_template('admin.html',msg = msg)
    else:
        return redirect(url_for("adminlogin")) 

@app.route("/addcandidate.html",methods = ['GET','POST'])
def add():
    """ This view will add an candidate for a particular election by using Election's unique id.
    """
    if "admin" in session:
        msg=None
        if request.method=="POST":
            name = request.form['name1']
            id = request.form['id']
            candid = request.form['candid']
            age = request.form['age']
            mobile = request.form['mobile']
            email = request.form['email']
            conn = sqlite3.connect("ivote.db")
            c = conn.cursor()
            c.execute("SELECT * from election WHERE electionid = '"+id+"'")
            r = c.fetchall()
            if len(r)<1:
                msg = "Election with this id doesn't exist"
            else :
                c.execute("INSERT INTO candidate VALUES('"+name+"','"+id+"','"+candid+"','"+age+"','"+mobile+"','"+email+"')")
                conn.commit()
                conn.close()
                msg = "Candidate Added"
        return render_template('addcandidate.html', msg=msg)
    else:
        return redirect(url_for("adminlogin"))



@app.route("/results.html",methods=['GET','POST'])
def result():
    """ This view will show all the elections and let the admin request for the result of a election.
    """
    if "admin" in session:
        r=""
        conn = sqlite3.connect("ivote.db")
        c = conn.cursor()
        c.execute("SELECT * FROM election")
        r = c.fetchall()
        return render_template('results.html',r = r)
    else :
        return redirect(url_for("adminlogin"))

@app.route("/show<int:id>")
def viewresults(id):
    """ This view will show the Result for the election which is choosen from "result()" function.
    """
    if "admin" in session:
        r=""
        p=str(id)
        conn = sqlite3.connect("ivote.db")
        c = conn.cursor()
        c.execute("SELECT * from result WHERE election_id = '"+p+"'")
        r = c.fetchall()
        return render_template("show.html",r =r )
    else:
        return redirect(url_for("adminlogin"))


""" Voter Code Started"""


@app.route("/voter.html",methods=['GET','POST'])
def voter():
    """ Home page for voter after login. This view will let voter view all the elections.
        And let voter vote for election.
    """
    if "voter" in session:
        r=""
        conn = sqlite3.connect("ivote.db")
        c = conn.cursor()
        c.execute("SELECT * FROM election")
        r = c.fetchall()
        return render_template('voter.html',r=r)
    else:
        return redirect(url_for("login"))

@app.route("/voterresult.html",methods=['GET','POST'])
def results():
    """ This view will let voters view all elections and let them request to know the result of requested election.
    """
    if "voter" in session:
        r=""
        conn = sqlite3.connect("ivote.db")
        c = conn.cursor()
        c.execute("SELECT * FROM election")
        r = c.fetchall()
        return render_template('voterresult.html',r = r)
    else :
        return redirect(url_for("login"))

@app.route("/logout")
def logout():
    """ This view will let admin and voter to logout from their sessions. 
    """
    session.clear()
    return redirect(url_for("login"))

@app.route("/genResult.html",methods=["GET","POST"])
def genresult():
    if "admin" in session:
        msg=""
        if request.method=="POST":
            GR = generateResults()
            id = request.form['id1']
            msg=GR.genResult(id)
        return render_template("genResult.html",msg=msg)
    else:
        return redirect(url_for("adminlogin"))

@app.route("/viewblockchain.html")
def viewblockchain():
    conn = sqlite3.connect("ivote.db")
    c = conn.cursor()
    c.execute("SELECT electionid FROM election")
    r = c.fetchall()
    allbc=[]
    for i in r:
        fle = Path("static/blockchain/"+str(i[0])+".txt")
        allbc.append("static/blockchain/"+str(i[0])+".txt")
        fle.touch(exist_ok=True)
        f = open(fle)
    conn.commit()
    conn.close()
    return render_template('viewblockchain.html',allbc=allbc) 

@app.route("/Voting.html",methods=["GET","POST"])
def Vote_give():
    if request.method=="POST":
        id = request.form['id']
        id2 = request.form['id2']
        conn = sqlite3.connect("ivote.db")
        c = conn.cursor()
        c.execute("CREATE TABLE IF NOT EXISTS election"+str(id)+"(secret_code TEXT ,name_of_blockchain TEXT,voter_id TEXT,vote_given TEXT)")
        r1 = random.randint(0, 100000)
        voter_id=session["voterid"]
        c.execute("select * from election"+str(id)+ " where voter_id='"+str(voter_id)+"'")
        rs=c.fetchall()
        B=Block(0,0,0,0)
        if(len(rs)==0):
            c.execute("select * from candidate where electionid='"+str(id)+"' and candidateid='"+str(id2)+"'")
            rs=c.fetchall()
            if(len(rs)==0):
                return render_template('Voting.html',msg="candidate not exist!")
            print("insert into election"+str(id)+" values('"+str(r1)+"','"+str(id)+"','"+str(voter_id)+"','"+str(id2)+"')")
            c.execute("insert into election"+str(id)+" values('"+str(r1)+"','"+str(id)+"','"+str(voter_id)+"','"+str(id2)+"')")
            conn.commit()
            conn.close()
            hash=B.addBlock(r1,str(id),voter_id,str(id2))
            return render_template('Voting.html',r1=r1,hash=hash,msg="voted succesfully!") 
    return render_template('Voting.html',msg="already voted!")

@app.route("/showelectionvoter<int:id>")
def showelectionvoter(id):
    if "voter" in session:
        p=str(id)
        conn = sqlite3.connect("ivote.db")
        c = conn.cursor()
        c.execute("SELECT * from election WHERE electionid = '"+p+"'")
        r = c.fetchall()
        return render_template("showelectionvoter.html",r =r )
    else :
        return redirect(url_for("login"))

@app.route("/showresultvoter<int:id>")
def showresultvoter(id):
    if "voter" in session:
        r=""
        p=str(id)
        conn = sqlite3.connect("ivote.db")
        c = conn.cursor()
        c.execute("SELECT * from result WHERE election_id = '"+p+"'")
        r = c.fetchall()
        return render_template("showresultvoter.html",r =r )
    else:
        return redirect(url_for("login"))


if __name__=="__main__":
    app.run(debug=True)