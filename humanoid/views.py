from flask.views import View
from robotics.decorators import analytics


class TemplateView(View):

    def __init__(self, template_name):
        self.template_name = template_name

    @analytics("web_response_time")
    def dispatch_request(self):
        from flask import render_template
        #from flask import current_app as app

        '''
        return render_template(self.template_name,
            github=app.config["GITHUB"],
            twitter=app.config["TWITTER"],
            database=app.config["DATABASE"]
        )
        '''
        return render_template(self.template_name)
