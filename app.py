from flask import Flask, render_template, make_response, url_for
from flask.ext.restful import reqparse, abort, Api, Resource
from os.path import join
import serial

app = Flask(__name__)
api = Api(app)

parser = reqparse.RequestParser()
parser.add_argument('task', type=str)

def abort_if_pin_does_not_exist(pin_id):
    if pin_id not in TODOS:
        abort(404, message="Todo {} doesn't exist".format(pin_id))

# http://playground.arduino.cc/interfacing/python#.UyD0yHVdUYp
def serial_example():
    ser = serial.Serial('/dev/tty.usbserial', 9600)
    while True:
        print ser.readline()
        # OR
        ser = serial.Serial('/dev/tty.usbserial', 9600)
        ser.write('5')


class PiPin(Resource):
    def get(self, pin_id):
        abort_if_pin_does_not_exist(pin_id)
        return TODOS[pin_id]

    def put(self, todo_id):
        args = parser.parse_args()
        task = {'task': args['task']}
        TODOS[todo_id] = task
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
        self.active = True
        try:
            import RPi.GPIO as GPIO
        except ImportError:
            self.active = False

    def pin_data(self, pin):
        GPIO.setmode(GPIO.BOARD)
        funcion = GPIO.gpio_function(pin)
        return {'function' : function, 'state' : 'GPIO.LOW'}

    def get(self):    
        #if self.active == False:
            # See "Fail fast"
            #return {0 : 0}
        
        #GPIO.setmode(GPIO.BCM)
        
        pin_range = [24, 25]
        pins = {}
        
        for pin in pin_range:
            pins[pin] = self.pin_data(pin)
            
        return pins
        
    def post(self):
        args = parser.parse_args()
        print(args)
        #pin_number = 
        
        # EXAMPLE:
        args = parser.parse_args()
        todo_id = 'todo%d' % (len(TODOS) + 1)
        TODOS[todo_id] = {'task': args['task']}
        return TODOS[todo_id], 201


class App(Resource):
    def get(self):
        return make_response(render_template('index.html'))

@app.route('/js/<path:path>')
def static_js(path):
    # send_static_file will guess the correct MIME type
    return app.send_static_file(join('js', path))

@app.route('/css/<path:path>')
def static_css(path):
    # send_static_file will guess the correct MIME type
    return app.send_static_file(join('css', path))

# Setup the Api resource routing
api.add_resource(App, '/')

api.add_resource(PiPins, '/gpio')
api.add_resource(PiPin, '/gpio/<string:pin_id>')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
