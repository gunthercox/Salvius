from flask import Flask, render_template, make_response, url_for, jsonify, request
from flask.ext.restful import abort, Api, Resource

from robot import Robot, RobotSerializer
from robot.body import BodySerializer
from robot.arm import ArmSerializer
from robot.arm.shoulder import ShoulderSerializer
from robot.arm.elbow import ElbowSerializer
from robot.arm.wrist import WristSerializer
from robot.arm.hand import HandSerializer, FingerSerializer
from robot.speech import Speech

from os.path import join

gpio_available = True

try:
    import RPi.GPIO as GPIO
except RuntimeError:
    # A RuntimeError is returned if the current device does not have GPIO pins.
    gpio_available = False

# Create the default robot
robot = Robot("Salvius")
robot.default()

# Create flask app
app = Flask(__name__)
api = Api(app)


class PiPin(Resource):
    def get(self, pin_id):
        # abort if pin does not exist
        if pin_id not in SOME_LIST_OF_PINS:
            abort(404, message="Pin {} doesn't exist".format(pin_id))
        return TODOS[pin_id]

    def put(self, pin_id):
        args = parser.parse_args()
        task = {'task': args['task']}
        TODOS[pin_id] = task
        return task, 201


class PiPins(Resource):
    """
    Returns a list of pin function for all pins:
    GPIO.INPUT, GPIO.OUTPUT, GPIO.SPI, GPIO.I2C,
    GPIO.PWM, GPIO.SERIAL, GPIO.UNKNOWN
    Returns a key and value of zero if the import for
    RPi.GPIO fails. Otherwise it will return the value
    and function for the specified pins.
    """

    def __init__(self):
        super(PiPins, self).__init__()

    def pin_data(self, pin):
        GPIO.setmode(GPIO.BOARD)
        funcion = GPIO.gpio_function(pin)
        return {'function' : function, 'state' : 'GPIO.LOW'}

    def get(self):
        if not gpio_available:
            # See "Fail fast"
            return {"warning" : "GPIO pins unavailable"}

        GPIO.setmode(GPIO.BCM)

        pin_range = [24, 25]
        pins = {}

        for pin in pin_range:
            pins[pin] = self.pin_data(pin)

        return pins

    def post(self):
        args = parser.parse_args()
        print(args)

        # EXAMPLE:
        pin_id = 'todo%d' % (len(TODOS) + 1)
        TODOS[pin_id] = {'task': args['task']}
        return TODOS[pin_id], 201


class App(Resource):
    def get(self):
        return make_response(render_template('index.html'))

class Test(Resource):
    def get(self):
        return make_response(render_template('test.html'))

@app.route('/api/robot/')
def api_robot():
    serialized = RobotSerializer(robot)
    return jsonify(serialized.data)

@app.route('/api/robot/body/')
def api_robot_body():
    serialized = BodySerializer(robot.body)
    return jsonify(serialized.data)

@app.route('/api/robot/body/arms/')
def api_robot_body_arms():

    arms = []

    for arm in robot.body.arms:
        serialized = ArmSerializer(arm)
        arms.append(serialized.data)

    return jsonify({"results": arms})

@app.route('/api/robot/body/arms/<int:id>')
def api_robot_body_arms_detail(id):

    arm = robot.body.arms[id]
    serialized = ArmSerializer(arm)

    return jsonify(serialized.data)

@app.route('/api/robot/body/arms/<int:id>/shoulder/')
def api_robot_body_arms_shouder(id):

    shoulder = robot.body.arms[id].shoulder
    serialized = ShoulderSerializer(shoulder)

    return jsonify(serialized.data)

@app.route('/api/robot/body/arms/<int:id>/hand/')
def api_robot_body_arms_hand(id):

    hand = robot.body.arms[id].hand
    serialized = HandSerializer(hand)

    return jsonify(serialized.data)

@app.route('/api/robot/body/arms/<int:id>/hand/fingers/')
def api_robot_body_arms_hand_fingers(id):

    fingers = []

    hand = robot.body.arms[id].hand

    for finger in hand.fingers:

        serialized = FingerSerializer(finger)
        fingers.append(serialized.data)

    return jsonify({"results": fingers})

@app.route('/api/robot/body/arms/<int:id>/hand/fingers/<int:finger_id>/', methods=["GET", "POST"])
def api_robot_body_arms_hand_fingers_finger(id, finger_id):

    finger = robot.body.arms[id].hand.fingers[finger_id]

    if request.method == "POST":
        value = request.get_json(force=True)["position"]
        finger.move(value)

    serialized = FingerSerializer(finger)

    return jsonify(serialized.data)

@app.route('/api/robot/body/arms/<int:id>/hand/thumb/', methods=["GET", "POST"])
def api_robot_body_arms_hand_thumb(id):

    thumb = robot.body.arms[id].hand.thumb

    if request.method == "POST":
        value = request.get_json(force=True)["position"]
        thumb.move(value)

    serialized = FingerSerializer(thumb)

    return jsonify(serialized.data)

@app.route('/js/<path:path>')
def static_js(path):
    # send_static_file sets the correct MIME type
    return app.send_static_file(join('js', path))

@app.route('/css/<path:path>')
def static_css(path):
    # send_static_file sets the correct MIME type
    return app.send_static_file(join('css', path))

# Setup the Api resource routing
api.add_resource(App, '/')
api.add_resource(Test, '/test/')

api.add_resource(Speech, '/api/speech/')

api.add_resource(PiPins, '/api/gpio/')
api.add_resource(PiPin, '/api/gpio/<string:pin_id>')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
