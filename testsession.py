from flask import Flask, render_template, request, session, redirect, url_for
import mysql.connector
from werkzeug.datastructures import ImmutableMultiDict
from flask_dance.contrib.google import make_google_blueprint, google
from datetime import datetime, timedelta
from flask_caching import Cache
app = Flask(__name__)
cache = Cache(app, config={'CACHE_TYPE': 'simple'})
T = datetime.today()
app.secret_key = "supersekrit"
blueprint = make_google_blueprint(
    client_id="1047419096832-8ct7dc5lrh6ruo27i4s60t5b9mg4oj2f.apps.googleusercontent.com",
    client_secret="jTpznze7dZ3EbvxEldv-zO3r",
    scope=[
        'https://www.googleapis.com/auth/userinfo.email', 'https://www.googleapis.com/auth/userinfo.profile'
    ],
    redirect_url=('/google12')
)
app.register_blueprint(blueprint, url_prefix="/login")


@app.route("/")
def root():

    print("session out*****", session.get('username', False))
    return render_template("home.html")


@app.route("/login", methods=['POST', 'GET'])
def login_form():
    global T
    if request.method == 'POST':
        mydb = mysql.connector.connect(
         host="localhost",
         user="root",
         passwd="root",
         database="hisham")
        mycursor = mydb.cursor()
        username = request.form['username']
        session['username'] = request.form['username']
        password = request.form['password']
        mycursor.execute("SELECT username FROM userdata")
        myresult = mycursor.fetchall()
        e = [i[0] for i in myresult]
        mycursor.execute("SELECT password FROM userdata")
        myresult1 = mycursor.fetchall()
        w = [j[0] for j in myresult1]
        mydb.commit()
        tt = "invalid account!!!!"
        sql = "SELECT * FROM diary WHERE day = %s"
        to = str(datetime.today().strftime('%Y-%m-%d'))
        mycursor.execute(sql, (to,))
        if username in e:
            if password in w:
                return redirect(url_for('home_page'))
            else:
                return render_template("home.html", tt=tt)
        else:
            return render_template("home.html", tt=tt)


@app.route("/userhome")
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
        return(render_template('userhome.html', T=T, myresult=myresult,user=ses))


# previous date


@app.route('/dbfetch', methods=['POST', 'GET'])
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
        dte = ImmutableMultiDict(request.form)
        x = dte.to_dict(flat=False)
        adr = (x.get('dte', False)[0],)
        val = (adr[0], y[0])
        mycursor.execute(sql, val)
        myresult = mycursor.fetchall()
        t = adr[0]
        mydb.commit()
        return render_template('userhome.html', myresult=myresult, T=t)


@app.route('/submit', methods=['POST', 'GET'])
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
        dte = ImmutableMultiDict(request.form)
        x = dte.to_dict(flat=False)
        adr = (x.get('dte', False)[0],)
        con = request.form['cont']
        val = (y[0], adr[0], con)
        if(con):
            sql1 = "DELETE FROM diary WHERE day = %s AND userid= %s "
            val2 = (adr[0], y[0])
            mycursor.execute(sql1, val2)
            mycursor.execute(sql, val)
        else:
            mycursor.execute(sql, val)
        t = adr[0]
        sql1 = "SELECT * FROM diary WHERE day = %s AND userid= %s"
        val1 = (adr[0], y[0])
        mycursor.execute(sql1, val1)
        myresult = mycursor.fetchall()
        mydb.commit()
        return render_template('userhome.html', T=t, myresult=myresult)


@app.route('/prevfetch')
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
    global T
    T = T - timedelta(days=1)
    d = T
    dt = d.strftime('%Y-%m-%d')
    sql = "SELECT * FROM diary WHERE day = %s and userid= %s"
    adr = (dt,)
    val = (adr[0], y[0])
    mycursor.execute(sql, val)
    myresult = mycursor.fetchall()
    mydb.commit()
    return render_template('userhome.html', myresult=myresult, T=dt)


@app.route('/nxtfetch')
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
    T = T + timedelta(days=1)
    d = T
    dt = d.strftime('%Y-%m-%d')
    sql = "SELECT * FROM diary WHERE day = %s AND userid=%s "
    adr = (dt,)
    val = (adr[0], y[0])
    mycursor.execute(sql, val)
    myresult = mycursor.fetchall()
    mydb.commit()
    return render_template('userhome.html', myresult=myresult, T=T)


@app.route("/regform")
def registration_form():
    return render_template('regform.html')


@app.route('/newuser', methods=['POST', 'GET'])
def user_registration():
    global T
    if request.method == 'POST':
        mydb = mysql.connector.connect(
         host="localhost",
         user="root",
         passwd="root",
         database="hisham")
        mycursor = mydb.cursor()
        sql = "INSERT INTO userdata( name,username,email,password,phone) VALUES (%s, %s, %s, %s, %s)"
        name = request.form['name']
        username = request.form['username']
        session['username'] = request.form['username']
        mail = request.form['email']
        password = request.form['password']
        reptpassword = request.form['repeatpassword']
        phone = request.form['phone']
        val = (name, username, mail, password, phone)
        mycursor.execute(sql, val)
        mydb.commit()
        print(mycursor.rowcount, "record inserted.")
        return redirect(url_for('home_page'))


@app.route('/logout')
@cache.cached(timeout=5)
def logout():

    print("session out**", session['username'])
    # session.pop('username', None)
    if(google.token):
        token = blueprint.token["access_token"]
        resp = google.post(
        "https://accounts.google.com/o/oauth2/revoke",
        params={"token": token},
        headers={"Content-Type": "application/x-www-form-urlencoded"}
    )

        del google.token
    session.clear()

    return redirect(url_for('root'))

@app.route('/google12')
def google_login():

    if not google.authorized:
        return redirect(url_for("google.login"))
    resp = google.get("/oauth2/v2/userinfo",
           params={'token': app.blueprints['google'].token["access_token"]},
                      )

    email=resp.json()["email"]
    session['username']=str(email)
    return redirect(url_for('home_page'))




import os

os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'


if __name__ == '__main__':
    app.run(debug=True)
