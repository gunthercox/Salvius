from flask.views import View


class App(View):
    def dispatch_request(self):
        from flask import render_template
        return render_template("interface.html")


class Connect(View):
    def dispatch_request(self):
        from flask import render_template, url_for
        from flask import current_app as app
        from chaterbot.apis.github import GitHub

        #self.db = app.config['ROBOT'].db

        github = GitHub()
        github.authorize_url = github.make_authorization_url(app.config['GITHUB'])

        return render_template("connect.html", github=github)


class Hands(View):
    def dispatch_request(self):
        from flask import render_template
        return render_template("hands.html")


class Limbs(View):
    def dispatch_request(self):
        from flask import render_template
        return render_template("limbs.html")


class Sensors(View):
    def dispatch_request(self):
        from flask import render_template
        return render_template("sensors.html")


class Chat(View):
    def dispatch_request(self):
        from flask import render_template
        return render_template("chat.html")


class Settings(View):
    def dispatch_request(self):
        from flask import render_template
        return render_template("settings.html")
