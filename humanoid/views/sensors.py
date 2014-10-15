from flask.views import View
from flask.ext.restful import Resource
from flask import request, jsonify


class Sensors(View):

    def __init__(self):
        return super(Sensors, self).__init__()

    def dispatch_request(self):
        from flask import render_template
        return render_template("sensors.html")
