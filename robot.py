from flask import Flask, render_template, jsonify, request
from flask.views import View
from flask.ext.restful import Api

from robot import Robot, RobotSerializer
from robot.body import BodySerializer
from robot.arm import ArmSerializer
from robot.arm.shoulder import ShoulderSerializer
from robot.arm.elbow import ElbowSerializer
from robot.arm.wrist import WristSerializer
from robot.arm.hand import HandSerializer, FingerSerializer
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


class Test(View):
    def dispatch_request(self):
        return render_template("test.html")


@app.route("/api/robot/")
def api_robot():
    serialized = RobotSerializer(robot)
    return jsonify(serialized.data)

@app.route("/api/robot/body/")
def api_robot_body():
    serialized = BodySerializer(robot.body)
    return jsonify(serialized.data)

@app.route("/api/robot/body/arms/")
def api_robot_body_arms():

    arms = []

    for arm in robot.body.arms:
        serialized = ArmSerializer(arm)
        arms.append(serialized.data)

    return jsonify({"results": arms})

@app.route("/api/robot/body/arms/<int:id>")
def api_robot_body_arms_detail(id):

    arm = robot.body.arms[id]
    serialized = ArmSerializer(arm)

    return jsonify(serialized.data)

@app.route("/api/robot/body/arms/<int:id>/shoulder/")
def api_robot_body_arms_shouder(id):

    shoulder = robot.body.arms[id].shoulder
    serialized = ShoulderSerializer(shoulder)

    return jsonify(serialized.data)

@app.route("/api/robot/body/arms/<int:id>/hand/")
def api_robot_body_arms_hand(id):

    hand = robot.body.arms[id].hand
    serialized = HandSerializer(hand)

    return jsonify(serialized.data)

@app.route("/api/robot/body/arms/<int:id>/hand/fingers/")
def api_robot_body_arms_hand_fingers(id):

    fingers = []

    hand = robot.body.arms[id].hand

    for finger in hand.fingers:

        serialized = FingerSerializer(finger)
        fingers.append(serialized.data)

    return jsonify({"results": fingers})

@app.route("/api/robot/body/arms/<int:id>/hand/fingers/<int:finger_id>/", methods=["GET", "POST"])
def api_robot_body_arms_hand_fingers_finger(id, finger_id):

    finger = robot.body.arms[id].hand.fingers[finger_id]

    if request.method == "POST":
        value = request.get_json(force=True)["position"]
        finger.move(value)

    serialized = FingerSerializer(finger)

    return jsonify(serialized.data)

@app.route("/api/robot/body/arms/<int:id>/hand/thumb/", methods=["GET", "POST"])
def api_robot_body_arms_hand_thumb(id):

    thumb = robot.body.arms[id].hand.thumb

    if request.method == "POST":
        value = request.get_json(force=True)["position"]
        thumb.move(value)

    serialized = FingerSerializer(thumb)

    return jsonify(serialized.data)

app.add_url_rule("/", view_func=App.as_view("index"))
app.add_url_rule("/test/", view_func=Test.as_view("test"))

# Setup the Api resource routing
api.add_resource(Speech, "/api/speech/")
api.add_resource(PiPins, "/api/gpio/")
api.add_resource(PiPin, "/api/gpio/<string:pin_id>")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
