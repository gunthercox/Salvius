from flask.views import View
from flask_oauthlib.client import OAuth


oauth = OAuth()

twitter = oauth.remote_app(
    "twitter",
    base_url="https://api.twitter.com/1/",
    request_token_url="https://api.twitter.com/oauth/request_token",
    access_token_url="https://api.twitter.com/oauth/access_token",
    authorize_url="https://api.twitter.com/oauth/authenticate",
    app_key="TWITTER"
)

google = oauth.remote_app(
    "google",
    base_url="https://www.google.com/accounts/",
    authorize_url="https://accounts.google.com/o/oauth2/auth",
    request_token_url=None,
    request_token_params={"scope": "email"},
    access_token_url="https://accounts.google.com/o/oauth2/token",
    access_token_method="POST",
    app_key="GOOGLE"
)

disqus = oauth.remote_app(
    "disqus",
    base_url="https://disqus.com/api/2.0/",
    authorize_url="https://disqus.com/api/oauth/2.0/authorize/",
    request_token_url=None,
    access_token_url="https://disqus.com/api/oauth/2.0/access_token/",
    access_token_method="POST",
    app_key="DISQUS"
)

@twitter.tokengetter
def get_twitter_token(token=None):
    from flask import session
    return session.get("twitter_token")

@google.tokengetter
def get_google_token():
    from flask import session
    return session.get("google_token")

@disqus.tokengetter
def get_disqus_token():
    return session.get("disqus_token")


class GitHubConnectView(View):
    def dispatch_request(self):
        """
        OAuth callback from GitHub
        """
        from flask import session, url_for, request, flash, redirect
        from flask import current_app as app
        import requests

        if "logout" in request.args:
            if session.has_key("github_user"):
                del session["github_user"]

            if session.has_key("github_token"):
                del session["github_token"]
        else:
            code = request.args.get("code", "")

            data = {
                "client_id": app.config["GITHUB"]["CLIENT_ID"],
                "client_secret": app.config["GITHUB"]["CLIENT_SECRET"],
                "code": code
            }

            headers = {"Accept": "application/json"}

            response = requests.post("https://github.com/login/oauth/access_token",
                                     data=data, headers=headers)
            token_json = response.json()

            # Save the value in the databse
            db = app.config["ROBOT"].db
            db.data(key="github_token", value=token_json["access_token"])

            # Save the value in the session
            session["github_token"] = token_json["access_token"]

            # Save the username
            token = "token " + token_json["access_token"]
            user = requests.get("https://api.github.com/user", headers={"Authorization": token})
            session["github_user"] = user.json()["name"]

        return redirect("/connect/")


class TwitterAuthorizedView(View):
    decorators = [twitter.authorized_handler]

    def dispatch_request(self, resp):
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


class TwitterConnectView(View):
    def dispatch_request(self):
        from flask import session, url_for, request, redirect

        if "login" in request.args:
            return twitter.authorize(callback=url_for("twitter_authorized", next=request.args.get("next") or request.referrer or None))

        if "logout" in request.args:
            if session.has_key("twitter_user"):
                del session["twitter_user"]

            if session.has_key("twitter_token"):
                del session["twitter_token"]

        return redirect(request.args.get("next") or url_for("connect"))


class GoogleAuthorizedView(View):
    decorators = [google.authorized_handler]

    def dispatch_request(self, resp):
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


class GoogleConnectView(View):
    def dispatch_request(self):
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

class DisqusAuthorizedView(View):
    decorators = [disqus.authorized_handler]

    def dispatch_request(self, resp):
        from flask import session, url_for, request, flash, redirect
        next_url = request.args.get("next") or url_for("connect")
        if resp is None:
            flash("You denied the request to sign in.")
            return redirect(next_url)
     
        session["disqus_token"] = resp["access_token"], ""
        session["disqus_user"] = resp["username"]

        flash("A Disqus account has been connected.")
        return redirect(next_url)


class DisqusConnectView(View):
    def dispatch_request(self):
        from flask import session, url_for, request, redirect

        if "login" in request.args:
            callback = url_for("disqus_authorized", _external=True)
            return disqus.authorize(callback=callback)

        if "logout" in request.args:
            if session.has_key("disqus_token"):
                del session["disqus_token"]

        return redirect(request.args.get("next") or url_for("connect"))
