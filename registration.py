from flask import render_template, request, session, redirect, url_for,flash
import mysql.connector
from flask import Blueprint
from datetime import datetime
import smtplib
server = smtplib.SMTP('smtp.gmail.com', 587)
server.starttls()
from random import randint

appfile2 = Blueprint('appfile2', __name__)
T = datetime.today()


@appfile2.route("/regform")
def registration_form():
    return render_template('regform.html')


@appfile2.route("/emailvalidation", methods=['POST', 'GET'])
def email_validation():
    if request.method == 'POST':
        mydb = mysql.connector.connect(
            host="localhost",
            user="root",
            passwd="root",
            database="hisham")
        mycursor = mydb.cursor()
        name = request.form['name']
        session['name'] = name
        username = request.form['username']
        session['username'] = request.form['username']
        mail = request.form['email']
        session['mail'] = mail
        phone = request.form['phone']
        session['phone'] = phone
        mycursor.execute("SELECT username FROM userdata")
        myresult = mycursor.fetchall()
        e = [i[0] for i in myresult]
        mycursor.execute("SELECT email FROM userdata")
        myresult1 = mycursor.fetchall()
        e = [i[0] for i in myresult]
        f = [j[0] for j in myresult1]
        if username in e or mail in f:
            flash("user  already exist")
            return redirect(url_for('appfile2.registration_form1'))
        else:
            server.login("aruarunimac@gmail.com", "arunima007")
            ot = str(randint(1000, 9999))
            session['ot'] = ot
            session['username'] = username
            msg = "Hi this is your one time password" + " " + ot
            server.sendmail("aruarunimac@gmail.com", mail, msg)
            return render_template("emailotp.html")


@appfile2.route("/checkotp", methods=['POST', 'GET'])
def check_otp():
    if request.method == 'POST':
        ot = session['ot']
        otp = request.form['otp']
        if(ot==str(otp)):

            return render_template("password.html")
        else:
            flash("wrong otp")
            return render_template("emailotp.html")
    else:
        return '''<html><body><h1>404 Bad Request</h1></body></html>'''



@appfile2.route("/regform1")
def registration_form1():
    nam = session['name']
    user=session['username']
    pho=session['phone']
    return (render_template('testregform.html', nam=nam,user=user,pho=pho))


@appfile2.route('/newuser', methods=['POST', 'GET'])
def user_registration():
    global T
    if request.method == 'POST':
        mydb = mysql.connector.connect(
            host="localhost",
            user="root",
            passwd="root",
            database="hisham")
        mycursor = mydb.cursor()
        name = session['name']
        username = session['username']
        mail = session['mail']
        phone = session['phone']
        password = request.form['pass']
        confirm_password=request.form['confirmpass']
        if(password==confirm_password):
            sql = "INSERT INTO userdata( name,username,email,password,phone) VALUES (%s, %s, %s, %s, %s)"
            val = (name, username, mail, password, phone)
            mycursor.execute(sql, val)
            mydb.commit()
            print(mycursor.rowcount, "record inserted.")
            return redirect(url_for('appfile.home_page'))
        else:
            flash("check the password")
            return render_template("password.html")

