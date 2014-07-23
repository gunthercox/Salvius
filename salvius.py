from flask import Flask, render_template, jsonify, request
from flask.views import View
from flask.ext.restful import Api, Resource

from robot import Robot, RobotSerializer
from robot.body import BodySerializer, ArmsSerializer, LegsSerializer
from robot.arm import ArmSerializer
from robot.arm.shoulder import ShoulderSerializer
from robot.arm.elbow import ElbowSerializer
from robot.arm.wrist import WristSerializer
from robot.arm.hand import HandSerializer, FingersSerializer, FingerSerializer
from robot.leg import LegSerializer
from robot.leg.hip import HipSerializer
from robot.leg.knee import KneeSerializer
from robot.leg.ankle import AnkleSerializer
from robot.leg.foot import FootSerializer
from robot.head import HeadSerializer
from robot.torso import TorsoSerializer
from robot.speech import Speech
from robot.gpio import PiPin, PiPins


# Create flask app
app = Flask(__name__, static_folder='static', static_url_path='')
api = Api(app)

# Create the default robot
robot = Robot("Salvius")


class App(View):
    def dispatch_request(self):
        return render_template("index.html")


class ApiRobot(Resource):
    def get(self):
        serialized = RobotSerializer(robot)
        return jsonify(serialized.data)


class ApiBody(Resource):
    def get(self):
        serialized = BodySerializer(robot.body)
        return jsonify(serialized.data)


class ApiHead(Resource):
    def get(self):
        serialized = HeadSerializer(robot.body.head)
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
        wrist.set_attributes(json)

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


class ApiFoot(Resource):
    def get(self, leg_id):
        serialized = FootSerializer(robot.body.legs[leg_id].foot)
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


app.add_url_rule("/", view_func=App.as_view("app"))

# Setup the Api resource routing
api.add_resource(ApiRobot, "/api/robot/")
api.add_resource(ApiBody, "/api/robot/body/")
api.add_resource(ApiHead, "/api/robot/body/head/")
api.add_resource(ApiTorso, "/api/robot/body/torso/")

api.add_resource(ApiArms, "/api/robot/body/arms/")
api.add_resource(ApiArm, "/api/robot/body/arms/<int:arm_id>/")
api.add_resource(ApiShoulder, "/api/robot/body/arms/<int:arm_id>/shoulder/")
api.add_resource(ApiElbow, "/api/robot/body/arms/<int:arm_id>/elbow/")
api.add_resource(ApiWrist, "/api/robot/body/arms/<int:arm_id>/wrist/")
api.add_resource(ApiHand, "/api/robot/body/arms/<int:arm_id>/hand/")
api.add_resource(ApiFingers, "/api/robot/body/arms/<int:arm_id>/hand/fingers/")
api.add_resource(ApiFinger, "/api/robot/body/arms/<int:arm_id>/hand/fingers/<int:finger_id>/")
api.add_resource(ApiThumb, "/api/robot/body/arms/<int:arm_id>/hand/thumb/")

api.add_resource(ApiLegs, "/api/robot/body/legs/")
api.add_resource(ApiLeg, "/api/robot/body/legs/<int:leg_id>/")
api.add_resource(ApiHip, "/api/robot/body/legs/<int:leg_id>/hip/")
api.add_resource(ApiKnee, "/api/robot/body/legs/<int:leg_id>/knee/")
api.add_resource(ApiAnkle, "/api/robot/body/legs/<int:leg_id>/ankle/")
api.add_resource(ApiFoot, "/api/robot/body/legs/<int:leg_id>/foot/")

api.add_resource(Terminate, "/api/terminate/")

api.add_resource(Speech, "/api/speech/")
api.add_resource(PiPins, "/api/gpio/")
api.add_resource(PiPin, "/api/gpio/<string:pin_id>")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
