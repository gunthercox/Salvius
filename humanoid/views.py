from flask.views import View


class TemplateView(View):

    def __init__(self, template_name):
        self.template_name = template_name

    def dispatch_request(self):
        from flask import render_template
        return render_template(self.template_name)


class Connect(View):
    def dispatch_request(self):
        from flask import render_template, url_for
        from flask import current_app as app
        from chaterbot.apis.github import GitHub

        github = GitHub()
        github.authorize_url = github.make_authorization_url(app.config["GITHUB"])

        return render_template("connect.html", github=github)
