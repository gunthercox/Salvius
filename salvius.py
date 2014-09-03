from flask import Flask
from flask.ext.restful import Api
from flask_oauthlib.client import OAuth

from link import settings

from humanoid import views

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
    request_token_params={"scope": "https://www.googleapis.com/auth/userinfo.email"},
    access_token_url="https://accounts.google.com/o/oauth2/token",
    access_token_method="POST",
    consumer_key=settings.GOOGLE["CLIENT_ID"],
    consumer_secret=settings.GOOGLE["CLIENT_SECRET"]
)

disqus = oauth.remote_app("disqus",
    base_url="https://disqus.com/api/3.0/",
    authorize_url="https://disqus.com/api/oauth/2.0/authorize/",
    request_token_url=None,
    access_token_url="https://disqus.com/api/oauth/2.0/access_token/",
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
    from link.settings import GITHUB
    from jsondb.db import Database

    # needs to be changed
    if "logout" not in request.args:

        code = request.args.get("code", "")

        data = {
            "client_id": GITHUB["CLIENT_ID"],
            "client_secret": GITHUB["CLIENT_SECRET"],
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
        session["github_user"] = "gunthercox"
        session["github_token"] = token_json["access_token"]

    if "logout" in request.args:
        if session.has_key("github_user"):
            del session["github_user"]

        if session.has_key("github_token"):
            del session["github_token"]

    return redirect('/connect/')


@app.route("/google/authorized/")
@google.authorized_handler
def google_authorized(resp):
    from flask import session, url_for, request, flash, redirect
    next_url = request.args.get("next") or url_for("connect")
    if resp is None:
        flash("You denied the request to sign in.")
        return redirect(next_url)

    session["google_token"] = resp["access_token"], ""

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

    flash("A Disqus account has been connected.")
    return redirect(next_url)

@app.route("/connect/disqus/")
def connect_disqus():
    from flask import session, url_for, request, redirect

    if "login" in request.args:
        callback = url_for(".disqus_authorized", _external=True)
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

app.add_url_rule("/", view_func=views.App.as_view("app"))
app.add_url_rule("/connect/", view_func=views.Connect.as_view("connect"))

app.add_url_rule("/api/", view_func=views.ApiBase.as_view("api"))

# Setup the Api resource routing
api.add_resource(views.ApiRobot, "/api/robot/")
api.add_resource(views.ApiBody, "/api/robot/body/")
api.add_resource(Neck, "/api/robot/body/neck/")
api.add_resource(Torso, "/api/robot/body/torso/")

api.add_resource(views.ApiArms, "/api/robot/body/arms/")
api.add_resource(views.ApiArm, "/api/robot/body/arms/<int:arm_id>/")
api.add_resource(Shoulder, "/api/robot/body/arms/<int:arm_id>/shoulder/")
api.add_resource(Elbow, "/api/robot/body/arms/<int:arm_id>/elbow/")
api.add_resource(Wrist, "/api/robot/body/arms/<int:arm_id>/wrist/")
api.add_resource(views.ApiHand, "/api/robot/body/arms/<int:arm_id>/hand/")
api.add_resource(views.ApiFingers, "/api/robot/body/arms/<int:arm_id>/hand/fingers/")
api.add_resource(Finger, "/api/robot/body/arms/<int:arm_id>/hand/fingers/<int:finger_id>/")
api.add_resource(Thumb, "/api/robot/body/arms/<int:arm_id>/hand/thumb/")

api.add_resource(Legs, "/api/robot/body/legs/")
api.add_resource(Leg, "/api/robot/body/legs/<int:leg_id>/")
api.add_resource(Hip, "/api/robot/body/legs/<int:leg_id>/hip/")
api.add_resource(Knee, "/api/robot/body/legs/<int:leg_id>/knee/")
api.add_resource(Ankle, "/api/robot/body/legs/<int:leg_id>/ankle/")

api.add_resource(views.Terminate, "/api/terminate/")
api.add_resource(Settings, "/api/settings/")
api.add_resource(Speech, "/api/speech/")
api.add_resource(Writing, "/api/writing/")

if __name__ == "__main__":
    app.config.update(
        DEBUG=True,
        SECRET_KEY="development",
        JSON_SORT_KEYS=False
    )
    app.run(host="0.0.0.0", port=8000)
