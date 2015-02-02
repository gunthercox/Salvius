from flask.views import View


class TemplateView(View):

    def __init__(self, template_name):
        self.template_name = template_name

    def dispatch_request(self):
        from flask import render_template
        return render_template(self.template_name)


class Connect(View):
    def dispatch_request(self):
        from flask import render_template
        from flask import current_app as app

        return render_template("connect.html",
            github=app.config["GITHUB"],
            twitter=app.config["TWITTER"],
            database=app.config["DATABASE"]
        )


class GitHubConnectView(View):

    def dispatch_request(self):
        """
        OAuth callback from GitHub
        """
        from flask import request, flash, redirect
        from flask import current_app as app
        import requests

        if "logout" in request.args:
            app.config["DATABASE"].delete("github_user")
            app.config["DATABASE"].delete("github_token")
        else:
            code = request.args.get("code", "")

            data = {
                "client_id": app.config["GITHUB"].github["CLIENT_ID"],
                "client_secret": app.config["GITHUB"].github["CLIENT_SECRET"],
                "code": code
            }

            headers = {"Accept": "application/json"}

            response = requests.post("https://github.com/login/oauth/access_token",
                                     data=data, headers=headers)
            token_json = response.json()

            # Save the value in the database
            app.config["DATABASE"]["github_token"] = token_json["access_token"]

            # Save the username
            token = "token " + token_json["access_token"]
            user = requests.get("https://api.github.com/user", headers={"Authorization": token})
            app.config["DATABASE"]["github_user"] = user.json()["name"]

            flash("You connected to GitHub as %s" % user.json()["name"])

        return redirect("/connect/")


class TwitterAuthorizedView(View):

    def dispatch_request(self):
        from flask import request, flash, redirect
        from flask import current_app as app
        import requests

        if "logout" in request.args:
            app.config["DATABASE"].delete("twitter_user")
            app.config["DATABASE"].delete("twitter_token")
        else:
            app.logger.debug(request.args)
            app.logger.debug(request)

            verifier = request.args["oauth_verifier"]

            twitter = app.config["TWITTER"]
            twitter.verify(verifier)
            '''
            if resp is None:
                flash("You denied the request to sign in.")
            else:
            '''
            app.config["DATABASE"]['twitter_token'] = (
                twitter.oauth_token,
                twitter.oauth_token_secret
            )
            username = twitter.get_name()
            app.config["DATABASE"]["twitter_user"] = username
            flash("You connected to Twitter as %s" % username)

        return redirect("/connect/")
