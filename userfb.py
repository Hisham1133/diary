from flask import render_template, request, session,json
import mysql.connector
from flask import Blueprint
from datetime import datetime
appfile7 = Blueprint('appfile7', __name__)
T = datetime.today()


@appfile7.route("/userhomefacebook")
def home_page():
    if 'username' in session:
        print("home page ", session['username'])
        global T
        mydb = mysql.connector.connect(
            host="localhost",
            user="root",
            passwd="root",
            database="hisham")
        mycursor = mydb.cursor()
        ses = session['username']
        sql12 = "SELECT id FROM userdata WHERE username = %s"
        adr12 = (ses,)
        print("fb")
        mycursor.execute(sql12, adr12)

        myresult12 = mycursor.fetchall()

        y12 = [i[0] for i in myresult12]
        if not y12:
            sql123 = "INSERT INTO userdata( username) VALUES (%s)"
            val = (ses, )
            mycursor.execute(sql123, val)
        sql1 = "SELECT id FROM userdata WHERE username = %s"
        adr1 = (ses,)
        mycursor.execute(sql1, adr1)
        id1 = mycursor.fetchall()
        y = [i[0] for i in id1]
        sql = "SELECT * FROM diary WHERE day = %s AND userid= %s "
        to = str(datetime.today().strftime('%Y-%m-%d'))
        val = (to, y[0])
        mycursor.execute(sql, val)
        myresult = mycursor.fetchall()
        mydb.commit()
        if (myresult != []):
            return (render_template('userhomefb.html', T=T, myresult=myresult, user=ses))
        else:
            return (render_template('userhomefb.html', T=T,  user=ses))


# previous date


@appfile7.route('/dbfetch', methods=['POST', 'GET'])
def prev_date():
    if request.method == 'POST':
        print("previw button *****", session.get('username', False))
        mydb = mysql.connector.connect(
            host="localhost",
            user="root",
            passwd="root",
            database="hisham"
        )
        mycursor = mydb.cursor()
        ses = session['username']
        sql1 = "SELECT id FROM userdata WHERE username = %s"
        adr1 = (ses,)
        mycursor.execute(sql1, adr1)
        id1 = mycursor.fetchall()
        y = [i[0] for i in id1]
        sql = "SELECT * FROM diary WHERE day = %s AND userid= %s"
        dte = request.get_data()
        x = dte.decode("utf-8")
        val = (x, y[0])
        mycursor.execute(sql, val)
        myresult = mycursor.fetchall()
        mydb.commit()
        if (myresult != []):
            t = str(myresult[0][1])
            t = t.replace('"', '')
            return json.dumps(t)
        else:
            return json.dumps(" ")


@appfile7.route('/submit', methods=['POST', 'GET'])
def submit_diary():
    if request.method == 'POST':
        mydb = mysql.connector.connect(
            host="localhost",
            user="root",
            passwd="root",
            database="hisham"
        )
        mycursor = mydb.cursor()
        ses = session['username']
        sql1 = "SELECT id FROM userdata WHERE username = %s"
        adr1 = (ses,)
        mycursor.execute(sql1, adr1)
        id1 = mycursor.fetchall()
        y = [i[0] for i in id1]
        sql = "INSERT INTO diary (userid,day, content) VALUES (%s, %s, %s)"
        adr = request.form['res1']
        con = request.form['res']
        val = (y[0], adr, con)
        if (con):
            sql1 = "DELETE FROM diary WHERE day = %s AND userid= %s "
            val2 = (adr, y[0])
            mycursor.execute(sql1, val2)
            mycursor.execute(sql, val)
        else:
            mycursor.execute(sql, val)
        sql1 = "SELECT * FROM diary WHERE day = %s AND userid= %s"
        val1 = (adr, y[0])
        mycursor.execute(sql1, val1)
        myresult = mycursor.fetchall()
        mydb.commit()
        return json.dumps(myresult[0][1])

#
# @appfile7.route('/prevfetch')
# def prev_diary():
#     print("*********", session['username'])
#     mydb = mysql.connector.connect(
#         host="localhost",
#         user="root",
#         passwd="root",
#         database="hisham"
#     )
#     mycursor = mydb.cursor()
#     ses = session['username']
#     sql1 = "SELECT id FROM userdata WHERE username = %s"
#     adr1 = (ses,)
#     mycursor.execute(sql1, adr1)
#     id1 = mycursor.fetchall()
#     y = [i[0] for i in id1]
#     global T
#     T = T - timedelta(days=1)
#     d = T
#     dt = d.strftime('%Y-%m-%d')
#     sql = "SELECT * FROM diary WHERE day = %s and userid= %s"
#     adr = (dt,)
#     val = (adr[0], y[0])
#     mycursor.execute(sql, val)
#     myresult = mycursor.fetchall()
#     mydb.commit()
#     return render_template('userhomefb.html', myresult=myresult, T=dt)
#
#
# @appfile7.route('/nxtfetch')
# def next_diary():
#     global T
#     print("**************", session['username'])
#     mydb = mysql.connector.connect(
#         host="localhost",
#         user="root",
#         passwd="root",
#         database="hisham"
#     )
#
#     mycursor = mydb.cursor()
#     ses = session['username']
#     sql1 = "SELECT id FROM userdata WHERE username = %s"
#     adr1 = (ses,)
#     mycursor.execute(sql1, adr1)
#     id1 = mycursor.fetchall()
#     y = [i[0] for i in id1]
#     T = T + timedelta(days=1)
#     d = T
#     dt = d.strftime('%Y-%m-%d')
#     sql = "SELECT * FROM diary WHERE day = %s AND userid=%s "
#     adr = (dt,)
#     val = (adr[0], y[0])
#     mycursor.execute(sql, val)
#     myresult = mycursor.fetchall()
#     mydb.commit()
#     return render_template('userhomefb.html', myresult=myresult, T=T)
