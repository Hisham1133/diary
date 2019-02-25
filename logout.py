from flask import session, redirect, url_for
from flask import Blueprint

appfile3 = Blueprint('appfile3', __name__)


@appfile3.route("/logout")
def logout():
    print("session out**", session['username'])
    session.pop('username', None)
    session.clear()
    return redirect(url_for('root'))
