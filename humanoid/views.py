from flask import jsonify, request
from flask.views import View
from flask.ext.restful import Resource

from humanoid import RobotSerializer
from humanoid.body import BodySerializer, ArmsSerializer, LegsSerializer
from humanoid.arm import ArmSerializer
from humanoid.arm.shoulder import ShoulderSerializer
from humanoid.arm.elbow import ElbowSerializer
from humanoid.arm.wrist import WristSerializer
from humanoid.arm.hand import HandSerializer, FingersSerializer, FingerSerializer
from humanoid.leg import LegSerializer
from humanoid.leg.hip import HipSerializer
from humanoid.leg.knee import KneeSerializer
from humanoid.leg.ankle import AnkleSerializer
from humanoid.neck import NeckSerializer
from humanoid.torso import TorsoSerializer

from humanoid.speech import Speech
from humanoid.settings import Settings

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


class ApiNeck(Resource):
    def get(self):
        serialized = NeckSerializer(robot.body.neck)
        return jsonify(serialized.data)


class ApiTorso(Resource):
    def get(self):
        serialized = TorsoSerializer(robot.body.torso)
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


class ApiElbow(Resource):

    def get(self, arm_id):
        serialized = ElbowSerializer(robot.body.arms[arm_id].elbow)
        return jsonify(serialized.data)

    def patch(self, arm_id):
        json = request.get_json(force=True)

        elbow = robot.body.arms[arm_id].elbow
        elbow.set_attributes(json)

        serialized = ElbowSerializer(elbow)
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


class ApiFinger(Resource):

    def get(self, arm_id, finger_id):
        finger = robot.body.arms[arm_id].hand.fingers[finger_id]
        serialized = FingerSerializer(finger)
        return jsonify(serialized.data)

    def patch(self, arm_id, finger_id):
        value = request.get_json(force=True)["position"]
        finger = robot.body.arms[arm_id].hand.fingers[finger_id]
        finger.move(value)
        serialized = FingerSerializer(finger)
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
        '''
        json = request.get_json(force=True)

        hip = robot.body.legs[leg_id].hip
        hip.set_attributes(json)

        serialized = HipSerializer(hip)
        return jsonify(serialized.data)
        '''


class ApiHip(Resource):

    def get(self, leg_id):
        serialized = HipSerializer(robot.body.legs[leg_id].hip)
        return jsonify(serialized.data)

    def patch(self, leg_id):
        json = request.get_json(force=True)

        hip = robot.body.legs[leg_id].hip
        hip.set_attributes(json)

        serialized = HipSerializer(hip)
        return jsonify(serialized.data)


class ApiKnee(Resource):

    def get(self, leg_id):
        serialized = KneeSerializer(robot.body.legs[leg_id].knee)
        return jsonify(serialized.data)

    def patch(self, leg_id):
        json = request.get_json(force=True)

        knee = robot.body.legs[leg_id].knee
        knee.set_attributes(json)

        serialized = KneeSerializer(knee)
        return jsonify(serialized.data)


class ApiAnkle(Resource):

    def get(self, leg_id):
        serialized = AnkleSerializer(robot.body.legs[leg_id].ankle)
        return jsonify(serialized.data)

    def patch(self, leg_id):
        json = request.get_json(force=True)

        ankle = robot.body.legs[leg_id].ankle
        ankle.set_attributes(json)

        serialized = AnkleSerializer(ankle)
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
