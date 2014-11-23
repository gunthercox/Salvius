from flask import jsonify, request
from flask.ext.restful import Resource

from humanoid import RobotSerializer, ArmsSerializer
from humanoid.arm import ArmSerializer
from humanoid.arm.hand import HandSerializer, FingersSerializer


class PhantExample(Resource):
    """
    This view can be used to track when the robot goes online.
    * Currently this view is not being used.
    """
    def get(self):
        from phant import Phant
        from salvius.settings import PHANT

        p = Phant(PHANT['PUBLIC_KEY'], 'status', private_key=PHANT['PRIVATE_KEY'])
        p.log("online")


class Base(Resource):
    def get(self):
        from flask import current_app as app

        robot = app.config['ROBOT']
        serialized = RobotSerializer(robot)
        return jsonify(serialized.data)


class Arms(Resource):
    def get(self):
        from flask import current_app as app

        robot = app.config['ROBOT']
        serialized = ArmsSerializer(robot)
        return jsonify(serialized.data)


class Arm(Resource):
    def get(self, arm_id):
        from flask import current_app as app

        robot = app.config['ROBOT']
        serialized = ArmSerializer(robot.arms[arm_id])
        return jsonify(serialized.data)


class Hand(Resource):
    def get(self, arm_id):
        from flask import current_app as app

        robot = app.config['ROBOT']
        serialized = HandSerializer(robot.arms[arm_id].hand)
        return jsonify(serialized.data)


class Fingers(Resource):
    def get(self, arm_id):
        from flask import current_app as app

        robot = app.config['ROBOT']
        serialized = FingersSerializer(robot.arms[arm_id].hand)
        return jsonify(serialized.data)


class Chat(Resource):

    def post(self):
        from flask import current_app as app

        json_data = request.get_json(force=True)
        key = u'text'

        chatbot = app.config['ROBOT'].chatbot
        data = {}

        if key in json_data:
            data["input"] = json_data[key]
            data["response"] = chatbot.get_response(json_data[key])

        return jsonify(data)


class Settings(Resource):

    def __init__(self):
        super(Settings, self).__init__()
        from flask import current_app as app

        self.db = app.config["ROBOT"].db

    def get(self):
        return self.db.data()

    def patch(self):
        json = request.get_json(force=True)
        self.db.data(dictionary=json)
        return self.db.data(), 201

    def put(self):
        json = request.get_json(force=True)
        self.db.data(dictionary=json)
        return self.db.data(), 201

    def delete(self):
        json = request.get_json(force=True)
        for key in json.keys():
            self.db.delete(key)
        return self.db.data(), 201


class Speech(Resource):
    """
    Process:
      1. String is posted to the speech api endpoint.
      2. String is validated to remove any unusual characters.
        --> Should numbers be converted to words?
      3. String is sent to an arduino using an I2C connection through the GPIO pins.
    """

    def __init__(self):
        return super(Speech, self).__init__()

    def post(self):
        json_data = request.get_json(force=True)
        speech_text = u'speech_text'

        if speech_text in json_data:
            data = json_data[speech_text]

            print(data)

            return json_data, 201

        return {"warning": "required value not provided in request"}, 500

    def get(self):
        return {"warning": "Method not allowed!!!"}, 405


class Writing(Resource):

    def __init__(self):
        return super(Writing, self).__init__()

    def post(self):
        json_data = request.get_json(force=True)
        text = u'text'

        if text in json_data:
            data = json_data[text]

            print(data)
            #TODO: Handle motor control for hand writing text

            return json_data, 201

        return {"warning": "required value not provided in request"}, 500


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
