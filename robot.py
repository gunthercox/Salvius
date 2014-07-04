from flask import Flask, render_template, make_response, url_for, jsonify
from flask.ext.restful import reqparse, abort, Api, Resource

from robot import Robot, RobotSerializer
from robot.body import Body, BodySerializer
from robot.arm import Arm, ArmSerializer
from robot.arm.shoulder import Shoulder, ShoulderSerializer
from robot.arm.elbow import Elbow, ElbowSerializer
from robot.arm.wrist import Wrist, WristSerializer
from robot.arm.hand import Hand, HandSerializer
from robot.arm.hand import Finger, FingerSerializer

from os.path import join
import serial

gpio_available = True

try:
    import RPi.GPIO as GPIO
except RuntimeError:
    '''
    A RuntimeError is returned if the current device does
    not have GPIO pins.
    '''
    gpio_available = False

# Build the robot here
robot = Robot("Salvius")

body = Body()
robot.setBody(body)

left_arm = Arm()
body.add_arm(left_arm)

leftShoulder = Shoulder()
left_arm.set_shoulder(leftShoulder)

leftElbow = Elbow()
leftElbow.move(1)
left_arm.set_elbow(leftElbow)

left_wrist = Wrist()
left_arm.set_wrist(left_wrist)

left_hand = Hand()
left_arm.set_hand(left_hand)

fingers = [Finger(), Finger(), Finger(), Finger()]
thumb = Finger()
for finger in fingers:
    left_hand.add_finger(finger)

left_hand.set_thumb(thumb)

# Create flask app
app = Flask(__name__)
api = Api(app)

parser = reqparse.RequestParser()
parser.add_argument('task', type=str)

def abort_if_pin_does_not_exist(pin_id):
    if pin_id not in SOME_LIST_OF_PINS:
        abort(404, message="Pin {} doesn't exist".format(pin_id))


class PiPin(Resource):
    def get(self, pin_id):
        abort_if_pin_does_not_exist(pin_id)
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

@app.route('/api/robot/')
def api_robot():
    serialized = RobotSerializer(robot)
    return jsonify(serialized.data)

@app.route('/api/robot/body/')
def api_robot_body():
    serialized = BodySerializer(body)
    return jsonify(serialized.data)

@app.route('/api/robot/body/arms/')
def api_robot_body_arms():
    serialized = ArmSerializer(left_arm)
    return jsonify(serialized.data)

@app.route('/api/robot/body/arms/shoulder/')
def api_robot_body_arms_shouder():
    shoulder = Shoulder()
    serialized = ShoulderSerializer(shoulder)
    return jsonify(serialized.data)

@app.route('/api/')
def api_root():
    return jsonify({"robot": "/api/robot/", "gpio": "/gpio/"})

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

api.add_resource(PiPins, '/gpio/')
api.add_resource(PiPin, '/gpio/<string:pin_id>')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
