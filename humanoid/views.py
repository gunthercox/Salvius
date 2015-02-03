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
