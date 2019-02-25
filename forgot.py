from flask import render_template, request, session, redirect, url_for,flash
import mysql.connector
from flask import Blueprint
appfile8 = Blueprint('appfile8', __name__)
import smtplib
server = smtplib.SMTP('smtp.gmail.com', 587)
server.starttls()
from random import randint

@appfile8.route("/forgot", methods=['POST', 'GET'])
def forgot():
    return render_template("forgot.html")


@appfile8.route("/otp", methods=['POST', 'GET'])
def otp():
    if request.method == 'POST':
            mydb = mysql.connector.connect(
            host="localhost",
            user="root",
            passwd="root",
            database="hisham")
            mycursor = mydb.cursor()
            mail = request.form['email']
            username = request.form['username']
            sql = "SELECT email FROM userdata WHERE username = %s"
            adr = (username,)
            mycursor.execute(sql, adr)
            myresult=mycursor.fetchall()
            mydb.commit()

            if  myresult:
                if (myresult[0][0] == mail):
                    server.login("aruarunimac@gmail.com", "arunima007")
                    ot = str(randint(1000, 9999))
                    session['ot'] = ot
                    session['username'] = username
                    msg = "Hi this is your one time password"+" "+ot
                    server.sendmail("aruarunimac@gmail.com",mail, msg)


                    return render_template("otp.html")
                else:
                    flash("username and email does not match!")
                    return render_template("forgot.html")
            else:
                flash("username and email does not match!")
                return render_template("forgot.html")

    else:
        return render_template("home.html")


@appfile8.route("/newpassword", methods=['POST', 'GET'])
def newpassword():
    if request.method == 'POST':
        ot = session['ot']
        username = session['username']
        otp = request.form['otp']

        if(ot==str(otp)):
            return render_template("newpassword.html")
        else:
            flash("wrong otp")
            return render_template("otp.html")
    else:
        return render_template()

@appfile8.route("/passwordchanged", methods=['POST', 'GET'])
def passwordchanged():
    if request.method == 'POST':
        mydb = mysql.connector.connect(
            host="localhost",
            user="root",
            passwd="root",
            database="hisham")
        mycursor = mydb.cursor()
        password = request.form['pass']
        confirm_password=request.form['confirmpass']
        if(password == confirm_password):
            sql = "UPDATE userdata SET password = %s WHERE username = %s"
            val = (password, session['username'])
            mycursor.execute(sql, val)
            mydb.commit()
            print("password changed")
            session.pop('ot', None)
            session.pop('username', None)

            return render_template("home.html")
        else:
            flash("check the password")
            return render_template("newpassword.html")
    else:
        return '''<html><body><h1>404 Bad Request</h1></body></html>'''

