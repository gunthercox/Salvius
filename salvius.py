from flask import Flask
from flask.ext.restful import Api
from flask_oauthlib.client import OAuth

from humanoid import views
from humanoid.views import chat
from humanoid.views import sensors

from humanoid.neck import Neck
from humanoid.torso import Torso

from humanoid.leg import Legs, Leg

from humanoid.arm.shoulder import Shoulder
from humanoid.arm.elbow import Elbow
from humanoid.arm.wrist import Wrist
from humanoid.arm.hand import Finger
from humanoid.arm.hand import Thumb

from humanoid.leg.hip import Hip
from humanoid.leg.knee import Knee
from humanoid.leg.ankle import Ankle

from humanoid.speech import Speech
from humanoid.writing import Writing
from humanoid.settings import Settings

class Set(object):
    """
    This class is a fix for the fact that a settings.py file is not
    included in the repo, so when tests are run it throws import erros.
    """
    def __init__(self):
        self.DEBUG = True
        self.GITHUB = {"CLIENT_ID": "x", "CLIENT_SECRET": "y"}
        self.TWITTER = {"CONSUMER_KEY": "x", "CONSUMER_SECRET": "y"}
        self.GOOGLE = {"CLIENT_ID": "x", "CLIENT_SECRET": "y"}
        self.DISQUS = {"API_KEY": "x", "API_SECRET": "y"}
        self.PHANT = {"PUBLIC_KEY": "x", "PRIVATE_KEY": "y"}
try:
    import settings
except ImportError:
    settings = Set()

# Create flask app
app = Flask(__name__, static_folder="static", static_url_path="")
api = Api(app)
oauth = OAuth()

twitter = oauth.remote_app('twitter',
    base_url='https://api.twitter.com/1/',
    request_token_url='https://api.twitter.com/oauth/request_token',
    access_token_url='https://api.twitter.com/oauth/access_token',
    authorize_url='https://api.twitter.com/oauth/authenticate',
    consumer_key=settings.TWITTER["CONSUMER_KEY"],
    consumer_secret=settings.TWITTER["CONSUMER_SECRET"]
)

google = oauth.remote_app("google",
    base_url="https://www.google.com/accounts/",
    authorize_url="https://accounts.google.com/o/oauth2/auth",
    request_token_url=None,
    request_token_params={"scope": "email"},
    access_token_url="https://accounts.google.com/o/oauth2/token",
    access_token_method="POST",
    consumer_key=settings.GOOGLE["CLIENT_ID"],
    consumer_secret=settings.GOOGLE["CLIENT_SECRET"]
)

disqus = oauth.remote_app("disqus",
    base_url="https://disqus.com/api/2.0/",
    authorize_url="https://disqus.com/api/oauth/2.0/authorize/",
    request_token_url=None,
    access_token_url="https://disqus.com/api/oauth/2.0/access_token/",
    access_token_method="POST",
    consumer_key=settings.DISQUS["API_KEY"],
    consumer_secret=settings.DISQUS["API_SECRET"]
)

@app.route("/twitter/authorized/")
@twitter.authorized_handler
def twitter_authorized(resp):
    from flask import session, url_for, request, flash, redirect
    next_url = request.args.get("next") or url_for("connect")
    if resp is None:
        flash("You denied the request to sign in.")
        return redirect(next_url)

    session['twitter_token'] = (
        resp['oauth_token'],
        resp['oauth_token_secret']
    )
    session['twitter_user'] = resp['screen_name']
    flash('You were signed in as %s' % resp['screen_name'])
    return redirect(next_url)


@app.route("/connect/twitter/")
def connect_twitter():
    from flask import session, url_for, request, redirect

    if "login" in request.args:
        return twitter.authorize(callback=url_for("twitter_authorized", next=request.args.get("next") or request.referrer or None))

    if "logout" in request.args:
        if session.has_key("twitter_user"):
            del session["twitter_user"]

        if session.has_key("twitter_token"):
            del session["twitter_token"]

    return redirect(request.args.get("next") or url_for("connect"))


@twitter.tokengetter
def get_twitter_token(token=None):
    from flask import session
    return session.get("twitter_token")


@app.route("/connect/github/")
def connect_github():
    """
    OAuth callback from GitHub
    """
    from flask import session, url_for, request, flash, redirect
    import requests
    from jsondb.db import Database

    if "logout" in request.args:
        if session.has_key("github_user"):
            del session["github_user"]

        if session.has_key("github_token"):
            del session["github_token"]
    else:
        code = request.args.get("code", "")

        data = {
            "client_id": settings.GITHUB["CLIENT_ID"],
            "client_secret": settings.GITHUB["CLIENT_SECRET"],
            "code": code
        }

        headers = {"Accept": "application/json"}

        response = requests.post("https://github.com/login/oauth/access_token",
                                 data=data, headers=headers)
        token_json = response.json()

        # Save the value in the databse
        db = Database("settings.db")
        db.data(key="github_token", value=token_json["access_token"])

        # Save the value in the session
        session["github_token"] = token_json["access_token"]

        # Save the username
        token = "token " + token_json["access_token"]
        user = requests.get("https://api.github.com/user", headers={"Authorization": token})
        session["github_user"] = user.json()["name"]

    return redirect("/connect/")


@app.route("/google/authorized/")
@google.authorized_handler
def google_authorized(resp):
    from flask import session, url_for, request, flash, redirect
    next_url = request.args.get("next") or url_for("connect")
    if resp is None:
        flash("You denied the request to sign in.")
        return redirect(next_url)

    session["google_token"] = resp["access_token"], ""

    user = google.get('https://www.googleapis.com/userinfo/v2/me')

    session["google_user"] = user.data["name"]

    # Not all google accounts have a username attached to them
    if not user.data["name"]:
        session["google_user"] = user.data["email"].split("@")[0]

    flash("A Google account has been connected.")
    return redirect(next_url)

@app.route("/connect/google/")
def connect_google():
    from flask import session, url_for, request, redirect

    if "login" in request.args:
        return google.authorize(callback=url_for('google_authorized', _external=True))

    if "logout" in request.args:
        if session.has_key("google_user"):
            del session["google_user"]

        if session.has_key("google_oauthtok"):
            del session["google_oauthtok"]

        if session.has_key("google_token"):
            del session["google_token"]

    return redirect(request.args.get("next") or url_for("connect"))

@google.tokengetter
def get_google_token():
    from flask import session
    return session.get("google_token")


@app.route("/disqus/authorized/")
@disqus.authorized_handler
def disqus_authorized(resp):
    from flask import session, url_for, request, flash, redirect
    next_url = request.args.get("next") or url_for("connect")
    if resp is None:
        flash("You denied the request to sign in.")
        return redirect(next_url)
 
    session["disqus_token"] = resp["access_token"], ""
    session["disqus_user"] = resp["username"]

    flash("A Disqus account has been connected.")
    return redirect(next_url)

@app.route("/connect/disqus/")
def connect_disqus():
    from flask import session, url_for, request, redirect

    if "login" in request.args:
        callback = url_for("disqus_authorized", _external=True)
        return disqus.authorize(callback=callback)

    if "logout" in request.args:
        if session.has_key("disqus_token"):
            del session["disqus_token"]

    return redirect(request.args.get("next") or url_for("connect"))

@disqus.tokengetter
def get_disqus_token():
    return session.get("disqus_token")


@app.route('/test/')
def get_tokens():
    # Delete this method later
    from flask import session
    cookie = str(dict(session))
    return cookie

app.add_url_rule("/interface/", view_func=views.App.as_view("app"))
app.add_url_rule("/limbs/", view_func=views.Limbs.as_view("limbs"))
app.add_url_rule("/connect/", view_func=views.Connect.as_view("connect"))
app.add_url_rule("/chat/", view_func=chat.Chat.as_view("chat"))
app.add_url_rule("/sensors/", view_func=sensors.Sensors.as_view("sensors"))
app.add_url_rule("/settings/", view_func=views.Settings.as_view("setting"))

# Setup the Api resource routing
api.add_resource(views.ApiBase, "/api/")
api.add_resource(Neck, "/api/neck/")
api.add_resource(Torso, "/api/torso/")

api.add_resource(views.ApiArms, "/api/arms/")
api.add_resource(views.ApiArm, "/api/arms/<int:arm_id>/")
api.add_resource(Shoulder, "/api/arms/<int:arm_id>/shoulder/")
api.add_resource(Elbow, "/api/arms/<int:arm_id>/elbow/")
api.add_resource(Wrist, "/api/arms/<int:arm_id>/wrist/")
api.add_resource(views.ApiHand, "/api/arms/<int:arm_id>/hand/")
api.add_resource(views.ApiFingers, "/api/arms/<int:arm_id>/hand/fingers/")
api.add_resource(Finger, "/api/arms/<int:arm_id>/hand/fingers/<int:finger_id>/")
api.add_resource(Thumb, "/api/arms/<int:arm_id>/hand/thumb/")

api.add_resource(Legs, "/api/legs/")
api.add_resource(Leg, "/api/legs/<int:leg_id>/")
api.add_resource(Hip, "/api/legs/<int:leg_id>/hip/")
api.add_resource(Knee, "/api/legs/<int:leg_id>/knee/")
api.add_resource(Ankle, "/api/legs/<int:leg_id>/ankle/")

api.add_resource(views.Terminate, "/api/terminate/")
api.add_resource(Settings, "/api/settings/")
api.add_resource(Speech, "/api/speech/")
api.add_resource(Writing, "/api/writing/")
api.add_resource(chat.ChatApi, "/api/chat/")

if __name__ == "__main__":
    app.config.update(
        DEBUG=True,
        SECRET_KEY="development",
        JSON_SORT_KEYS=False
    )
    app.config['GITHUB'] = settings.GITHUB
    app.run(host="0.0.0.0", port=8000)
