from flask import Flask, url_for, redirect,render_template
from flask_dance.contrib.facebook import make_facebook_blueprint,facebook
import ast

app = Flask(__name__)
app.config['SERVER_NAME'] = 'localhost:5000'
app.secret_key = "<ISHOULDBESOMETHING>"
batman_example = make_facebook_blueprint(
    client_id="432901240580973",
    client_secret="7378ae063eb18e3f3d40893c95c3ef0c",
)
app.register_blueprint(batman_example, url_prefix="/login")
print(dir(make_facebook_blueprint()))

@app.route("/")
def index():
    if not batman_example.session.authorized:
        return redirect(url_for("facebook.login"))
    resp = batman_example.session.get("me")
    dic=ast.literal_eval(resp.text)
    print(dic)
    print(dic['name'])
    assert resp.ok
    return render_template("home.html")
import os

os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'

if __name__ == "__main__":
    app.run( debug=True)