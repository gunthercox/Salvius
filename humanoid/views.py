from flask import jsonify, request
from flask.views import View
from flask.ext.restful import Resource

from humanoid import RobotSerializer
from humanoid.body import BodySerializer, ArmsSerializer, LegsSerializer
from humanoid.arm import ArmSerializer
from humanoid.arm.shoulder import ShoulderSerializer
from humanoid.arm.wrist import WristSerializer
from humanoid.arm.hand import HandSerializer, FingersSerializer, FingerSerializer
from humanoid.leg import LegSerializer

from robot import robot


class App(View):
    def dispatch_request(self):
        from flask import render_template
        return render_template("index.html")


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


class ApiShoulder(Resource):
    def get(self, arm_id):
        serialized = ShoulderSerializer(robot.body.arms[arm_id].shoulder)
        return jsonify(serialized.data)

    def patch(self, arm_id):
        json = request.get_json(force=True)

        shoulder = robot.body.arms[arm_id].shoulder
        shoulder.set_attributes(json)

        serialized = ShoulderSerializer(shoulder)
        return jsonify(serialized.data)


class ApiWrist(Resource):

    def get(self, arm_id):
        serialized = WristSerializer(robot.body.arms[arm_id].wrist)
        return jsonify(serialized.data)

    def patch(self, arm_id):
        json = request.get_json(force=True)

        wrist = robot.body.arms[arm_id].wrist
        wrist.set_attributes(json)

        serialized = WristSerializer(wrist)
        return jsonify(serialized.data)


class ApiHand(Resource):
    def get(self, arm_id):
        serialized = HandSerializer(robot.body.arms[arm_id].hand)
        return jsonify(serialized.data)


class ApiFingers(Resource):
    def get(self, arm_id):
        serialized = FingersSerializer(robot.body.arms[arm_id].hand)
        return jsonify(serialized.data)


class ApiThumb(Resource):

    def get(self, arm_id):
        serialized = FingerSerializer(robot.body.arms[arm_id].hand.thumb)
        return jsonify(serialized.data)

    def patch(self, arm_id):
        value = request.get_json(force=True)["position"]
        thumb = robot.body.arms[arm_id].hand.thumb
        thumb.move(value)
        serialized = FingerSerializer(thumb)
        return jsonify(serialized.data)


class ApiLegs(Resource):

    def get(self):
        serialized = LegsSerializer(robot.body)
        return jsonify(serialized.data)


class ApiLeg(Resource):

    def get(self, leg_id):
        serialized = LegSerializer(robot.body.legs[leg_id])
        return jsonify(serialized.data)

    def patch(self, leg_id):
        # There is curretly no way to patch to nested items
        pass


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
