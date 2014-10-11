from flask.ext.restful import Resource, abort

gpio_available = True

try:
    import RPi.GPIO as GPIO
except RuntimeError:
    # A RuntimeError is returned if the current device does not have GPIO pins.
    gpio_available = False


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
