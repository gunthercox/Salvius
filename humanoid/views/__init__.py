from flask import jsonify, request
from flask.views import View
from flask.ext.restful import Resource

from humanoid import RobotSerializer
from humanoid.body import BodySerializer, ArmsSerializer
from humanoid.arm import ArmSerializer
from humanoid.arm.hand import HandSerializer, FingersSerializer

from humanoid import Robot


robot = Robot()

class App(View):
    def dispatch_request(self):
        from flask import render_template
        return render_template("index.html")


class Connect(View):

    def __init__(self):
        super(Connect, self).__init__()
        from jsondb.db import Database

        self.db = Database("settings.db")

    def dispatch_request(self):
        from flask import render_template, url_for
        from flask import current_app as app
        from link._github import GitHub

        github = GitHub()
        github.authorize_url = github.make_authorization_url(app.config['GITHUB'])

        return render_template("connect.html", github=github)


class Settings(View):
    def dispatch_request(self):
        from flask import render_template
        return render_template("settings.html")


class PhantExample(View):
    """
    This view can be used to track when the robot goes online.
    * Currently this view is not being used.
    """
    def dispatch_request(self):
        from phant import Phant
        from salvius.settings import PHANT

        p = Phant(PHANT['PUBLIC_KEY'], 'status', private_key=PHANT['PRIVATE_KEY'])
        p.log("online")


class ApiBase(View):

    def dispatch_request(self):
        from flask import render_template, url_for
        from salvius import app
        from humanoid.browsable_api import BrowsableApi
        output = []
        for rule in app.url_map.iter_rules():
            if not rule.arguments:
                url = url_for(rule.endpoint)
                
                if url.startswith("/api/"):
                    endpoint = str(rule.endpoint)
                    obj = BrowsableApi(endpoint, url)
                    output.append(obj)

        return render_template("browsable_api.html", endpoints=output)


class ApiRobot(Resource):
    def get(self):
        serialized = RobotSerializer(robot)
        return jsonify(serialized.data)


class ApiBody(Resource):
    def get(self):
        serialized = BodySerializer(robot.body)
        return jsonify(serialized.data)


class ApiArms(Resource):
    def get(self):
        serialized = ArmsSerializer(robot.body)
        return jsonify(serialized.data)


class ApiArm(Resource):
    def get(self, arm_id):
        serialized = ArmSerializer(robot.body.arms[arm_id])
        return jsonify(serialized.data)


class ApiHand(Resource):
    def get(self, arm_id):
        serialized = HandSerializer(robot.body.arms[arm_id].hand)
        return jsonify(serialized.data)


class ApiFingers(Resource):
    def get(self, arm_id):
        serialized = FingersSerializer(robot.body.arms[arm_id].hand)
        return jsonify(serialized.data)


class Terminate(Resource):
    """
    Endpoint to stop the server on the robot.
    This will stop commands from being processed,
    however it will not stop tasks running on parallel controllers.
    """
    def post(self):
        shutdown = request.environ.get('werkzeug.server.shutdown')
        if shutdown is None:
            raise RuntimeError('Not running with the Werkzeug Server')
        shutdown()
