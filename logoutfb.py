from flask import session, redirect, url_for
from flask_dance.consumer import OAuth2ConsumerBlueprint
from flask_dance.contrib.facebook import make_facebook_blueprint,facebook

from flask import Blueprint

appfile6 = Blueprint('appfile6', __name__)

batman_example = make_facebook_blueprint(
    client_id="432901240580973",
    client_secret="7378ae063eb18e3f3d40893c95c3ef0c",
    redirect_url=('/facebook')
)




@appfile6.route("/logoutfacebook")
def logoutfacebook():
    token = batman_example.token["access_token"]
    if (facebook.token):

        resp = facebook.post(
            # "https://graph.facebook.com/oauth/access_token/DELETE",
            "https://www.facebook.com/v3.2/dialog/oauth/DELETE",
            params={"access_token": token, "redirect_uri": "http://localhost:5000",
                    "client_id":session["username"]},
            headers={"Content-Type": "application/x-www-form-urlencoded"}
        )

        del facebook.token

    session.clear()
    return redirect(url_for('root'))
