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
                #session[]
                return redirect(url_for("voter"))

    return render_template('home.html')


@app.route('/signup.html',methods=['GET','POST'])
def signup():
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
                return redirect(url_for("admin")) 
    return  render_template('Login.html')


@app.route('/forgotPassword.html',methods=['GET','POST'])
def forgot():
    return  render_template('forgotPassword.html')


@app.route('/admin.html',methods = ['GET','POST'])
def admin():
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

@app.route("/addcandidate.html",methods = ['GET','POST'])
def add():
    if request.method=="POST":
        name = request.form['name1']
        id = request.form['id']
        candid = request.form['candid']
        age = request.form['age']
        mobile = request.form['mobile']
        email = request.form['email']
        conn = sqlite3.connect("ivote.db")
        c = conn.cursor()
        c.execute("INSERT INTO candidate VALUES('"+name+"','"+id+"','"+candid+"','"+age+"','"+mobile+"','"+email+"')")
        conn.commit()
        conn.close()
    return render_template('addcandidate.html')



@app.route("/results.html",methods=['GET','POST'])
def result():
    msg = None
    print("Working")
    if request.method=="POST":
        
        id = request.form['id']
        conn = sqlite3.connect("ivote.db")
        c = conn.cursor()
        c.execute("SELECT * from election WHERE electionid = '"+id+"'")
        r = c.fetchall()
        if len(r) >= 1:
            print("Working")
            return redirect(url_for("viewresults",id = id))
            
        else:
            msg = "Please enter correct ID"
    return render_template('results.html',msg = msg)

@app.route("/election",methods=['GET','POST'])
def election():
    id = request.form.get("id",None)
    return render_template('election.html')


@app.route("/voter.html",methods=['GET','POST'])
def voter():
    if request.method=="POST":
        id = request.form['id']
        conn = sqlite3.connect("ivote.db")
        c = conn.cursor()
        c.execute("SELECT * from election WHERE electionid = '"+id+"'")
        r = c.fetchall()
        if len(r) >= 1:
            return redirect(url_for("election",id = id))
    return render_template('voter.html')

@app.route("/voterresult.html")
def results():
    msg = None
    print("Working")
    if request.method=="POST":
        
        id = request.form['id']
        conn = sqlite3.connect("ivote.db")
        c = conn.cursor()
        c.execute("SELECT * from election WHERE electionid = '"+id+"'")
        r = c.fetchall()
        if len(r) >= 1:
            print("Working")
            return redirect(url_for("viewresults",id = id))
            
        else:
            msg = "Please enter correct ID"
    return render_template("voterresult.html",msg=msg)


@app.route("/view",methods=["GET","POST"])
def viewresults():
    id = request.form.get('id',None)
    print(id)
    return render_template("view.html")


@app.route("/logout")
def logout():
    return redirect(url_for("login"))

@app.route("/genResult.html",methods=["GET","POST"])
def genresult():
    msg=""
    if request.method=="POST":
        GR = generateResults()
        id = request.form['id1']
        msg=GR.genResult(id)
       
    return render_template("genResult.html",msg=msg)

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

@app.route("/Voting.html")
def Vote():
    if request.method=="POST":
        
        id = request.form['id']
        id2 = request.form['id2']
        conn = sqlite3.connect("ivote.db")
        c = conn.cursor()
        c.execute("CREATE TABLE IF NOT EXISTS election"+id2+"(secret_code TEXT ,name_of_blockchain TEXT,voter_id TEXT,vote_given TEXT)")
        r1 = random.randint(0, 100000)
        B=Block(1,0,0,0)
        hash=B.addBlock(r1,str(id),1,str(id2))
        return render_template('voter.html',r1=r1,hash=hash) 
    return render_template('Voting.html')


   


if __name__=="__main__":
    app.run(debug=True)
