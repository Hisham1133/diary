from flask import render_template, request, session, redirect, url_for,flash
import mysql.connector
from datetime import datetime
from flask import Blueprint
appfile1 = Blueprint('appfile1', __name__)
T = datetime.today()


@appfile1.route("/login", methods=['POST', 'GET'])
def login_form():
    global T
    if request.method == 'POST':
        mydb = mysql.connector.connect(
            host="localhost",
            user="root",
            passwd="root",
            database="hisham")
        mycursor = mydb.cursor(buffered=True)
        username = request.form['username']
        session['username'] = request.form['username']
        password = request.form['password']
        sql1 = ("SELECT * FROM userdata WHERE username= %s AND password= %s ")
        adr1 = (username, password,)
        mycursor.execute(sql1, adr1)
        myresult = mycursor.fetchall()
        tt = "invalid account!!!!"
        sql = "SELECT * FROM diary WHERE day = %s"
        to = str(datetime.today().strftime('%Y-%m-%d'))
        mycursor.execute(sql, (to,))
        if myresult:
            sql1 = "SELECT name FROM userdata WHERE username = %s"
            adr1 = (request.form['username'],)
            mycursor.execute(sql1, adr1)
            myresult2 = [j[0] for j in mycursor.fetchall()]
            session['name'] = myresult2[0]
            flash("login success")
            return redirect(url_for('appfile.home_page'))

        else:
             return render_template("home.html", tt=tt)
    else:
        return render_template("home.html")