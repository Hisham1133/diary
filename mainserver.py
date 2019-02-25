
from flask import Flask
import ast
import os
from user import *
from login import *
from registration import *
from logout import *
from usergoogle import *
from logoutgoogle import *
from logoutfb import *
from userfb import *
from forgot import *

app = Flask(__name__, static_url_path='',
            static_folder='static',
            template_folder='templates')
app.config['SERVER_NAME'] = 'localhost:5000'
app.register_blueprint(appfile)
app.register_blueprint(appfile1)
app.register_blueprint(appfile2)
app.register_blueprint(appfile3)
app.register_blueprint(appfile4)
app.register_blueprint(appfile5)
app.register_blueprint(appfile6)
app.register_blueprint(appfile7)
app.register_blueprint(appfile8)
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

batman_example = make_facebook_blueprint(
    client_id="432901240580973",
    client_secret="7378ae063eb18e3f3d40893c95c3ef0c",
    redirect_url=('/facebook')
)
app.register_blueprint(batman_example, url_prefix="/login")


@app.route("/")
def root():
    return render_template("home.html")


@app.route('/google12')
def google_login():
    if not google.authorized:
        return redirect(url_for("google.login"))
    resp = google.get("/oauth2/v2/userinfo",
                      params={'token': app.blueprints['google'].token["access_token"]},
                      )

    email = resp.json()["email"]
    session['username'] = str(email)
    return redirect(url_for('appfile4.home_page'))


@app.route("/facebook")
def index():

    if not facebook.authorized:
        return redirect(url_for("facebook.login"))
    resp = facebook.get("me", params={'token': app.blueprints['facebook'].token["access_token"]},)

    dic = ast.literal_eval(resp.text)
    session['username'] = str(dic['name'])

    assert resp.ok
    return redirect(url_for('appfile7.home_page'))


os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'

if __name__ == '__main__':
    app.run(debug=True)
