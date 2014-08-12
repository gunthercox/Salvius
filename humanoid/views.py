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


def get_token(code):
    import requests
    from link.settings import GITHUB
    from jsondb.db import Database

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
    db.data(key="github_access_token", value=token_json["access_token"])

    return token_json["access_token"]


class Connect(View):

    def __init__(self):
        super(Connect, self).__init__()
        from jsondb.db import Database

        self.db = Database("settings.db")

    def make_authorization_url(self):
        # Generate a random string for the state parameter
        # Save it for use later to prevent xsrf attacks
        from uuid import uuid4
        from link.settings import GITHUB
        import urllib

        state = str(uuid4())
        #save_created_state(state)
        #print("___STATE___", state)
        params = {
            "client_id": GITHUB["CLIENT_ID"],
            "scope": "repo, user",
            "state": state
        }
        url = "https://github.com/login/oauth/authorize?"
        url += urllib.urlencode(params)
        return url

    def dispatch_request(self):
        from flask import render_template
        from link._github import GitHub

        github = GitHub()
        github.is_authorize = self.db.data(key=github.token_key) is not None
        github.authorize_url = self.make_authorization_url()

        return render_template("connect.html", github=github)


class ApiBase(Resource):
    def get(self):
        from flask import url_for
        from salvius import app
        output = {}
        for rule in app.url_map.iter_rules():
            if not rule.arguments:
                url = url_for(rule.endpoint)
                output[str(rule.endpoint)] = url

        return jsonify(output)


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
