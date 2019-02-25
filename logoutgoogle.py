from flask import session, redirect, url_for

from flask_dance.contrib.google import make_google_blueprint, google

from flask import Blueprint

appfile5 = Blueprint('appfile5', __name__)
blueprint = make_google_blueprint(
    client_id="1047419096832-8ct7dc5lrh6ruo27i4s60t5b9mg4oj2f.apps.googleusercontent.com",
    client_secret="jTpznze7dZ3EbvxEldv-zO3r",
    scope=[
        "https://www.googleapis.com/auth/plus.me",
        "https://www.googleapis.com/auth/userinfo.email",

    ],
    redirect_url=('/google12')
)


@appfile5.route("/logoutgoogle")
def logoutgoogle():
    print("session out123**", session['username'])
    # session.pop('username', None)
    if (google.token):
        token = blueprint.token["access_token"]
        resp = google.post(
            "https://accounts.google.com/o/oauth2/revoke",
            params={"token": token},
            headers={"Content-Type": "application/x-www-form-urlencoded"}
        )

        del google.token
    session.clear()

    return redirect(url_for('root'))
