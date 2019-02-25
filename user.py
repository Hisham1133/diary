from flask import render_template, request, session,json,jsonify
import mysql.connector
from flask import Blueprint
from datetime import datetime,timedelta
appfile = Blueprint('appfile', __name__)
T = datetime.today()


@appfile.route("/userhome")
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
        nam = session['name']
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
        sql12 = "SELECT name FROM userdata WHERE username = %s"
        adr12 = (ses,)
        mycursor.execute(sql12, adr12)
        name = [j[0] for j in mycursor.fetchall()]
        if(myresult!=[]):
            u = myresult[0][1].replace("<br>","\n")

            return (render_template('userhome.html', T=T, myresult=u,myresult1=myresult[0][1], user=name[0], nam=nam))
        else:
            return (render_template('userhome.html', T=T,  user=name[0], nam=nam))
    else:
        return render_template("home.html")

# previous date


@appfile.route('/dbfetch', methods=['POST', 'GET'])
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
        if(myresult !=[]):
            t=str(myresult[0][1])
            # t = t.replace('"', '')
            return json.dumps(t)
        else:
            return json.dumps(" ")
    else:
        return '''<html><body><h1>404 Bad Request</h1></body></html>'''


@appfile.route('/submit', methods=['POST', 'GET'])
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
        con = con.rstrip()

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
    else:
        return '''<html><body><h1>404 Bad Request</h1></body></html>'''

@appfile.route('/prevfetch',  methods=['POST', 'GET'])
def prev_diary():
    print("*********", session['username'])
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
    dte = request.get_data()
    dte = dte.decode("utf-8")
    date = dte
    date = datetime.strptime(date, "%Y-%m-%d");

    d = date - timedelta(days=1)
    dt = d.strftime('%Y-%m-%d')
    sql = "SELECT * FROM diary WHERE day = %s and userid= %s"
    adr = (dt,)
    val = (adr[0], y[0])
    mycursor.execute(sql, val)

    myresult = mycursor.fetchall()

    lis = []
    if(myresult):
        lis.append(myresult[0][1])
        lis.append(dt)
    else:
        lis.append("  ")
        lis.append(dt)

    mydb.commit()

    return json.dumps(lis)


@appfile.route('/nxtfetch', methods=['POST', 'GET'])
def next_diary():
    global T
    print("**************", session['username'])
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
    dte = request.get_data()
    dte = dte.decode("utf-8")
    date = dte
    date = datetime.strptime(date, "%Y-%m-%d")

    d= date + timedelta(days=1)

    dt = d.strftime('%Y-%m-%d')
    sql = "SELECT * FROM diary WHERE day = %s AND userid=%s "
    adr = (dt,)
    val = (adr[0], y[0])
    mycursor.execute(sql, val)
    myresult = mycursor.fetchall()
    lis = []

    if (myresult):
        lis.append(myresult[0][1])
        lis.append(dt)

    else:
        lis.append("  ")
        lis.append(dt)
    mydb.commit()
    return json.dumps(lis)
