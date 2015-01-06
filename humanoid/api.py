from flask import request
from flask.views import MethodView


class Chat(MethodView):

    def post(self):
        from flask import current_app as app
        from flask import jsonify

        json_data = request.get_json(force=True)
        key = u'text'

        chatbot = app.config['CHATBOT']
        data = {}

        if key in json_data:
            data["input"] = json_data[key]
            data["response"] = chatbot.get_response(json_data[key])

        return jsonify(data)


class Settings(MethodView):

    def __init__(self):
        super(Settings, self).__init__()
        from flask import current_app as app

        self.db = app.config["ROBOT"].db

    def get(self):
        from flask import jsonify
        return jsonify(self.db.data())

    def patch(self):
        from flask import jsonify
        json = request.get_json(force=True)
        self.db.data(dictionary=json)
        return jsonify(self.db.data()), 201

    def put(self):
        from flask import jsonify
        json = request.get_json(force=True)
        self.db.data(dictionary=json)
        return jsonify(self.db.data()), 201

    def delete(self):
        from flask import jsonify
        json = request.get_json(force=True)
        for key in json.keys():
            self.db.delete(key)
        return jsonify(self.db.data()), 201


class Speech(MethodView):

    def post(self):
        from flask import jsonify
        from robotics.arduino import Arduino

        json_data = request.get_json(force=True)
        speech_text = u'speech_text'

        if speech_text in json_data:
            data = json_data[speech_text]

            text_to_speech_controller = Arduino("text_to_speech")
            text_to_speech_controller.write(data + "\n")

            return jsonify(json_data), 201

        return jsonify({"warning": "required value not provided in request"}), 500

    def get(self):
        from flask import abort
        abort(405)


class Writing(MethodView):

    def __init__(self):
        return super(Writing, self).__init__()

    def post(self):
        from flask import jsonify
        json_data = request.get_json(force=True)
        text = u'text'

        if text in json_data:
            data = json_data[text]

            print(data)
            #TODO: Handle motor control for hand writing text

            return jsonify(json_data), 201

        return jsonify({"warning": "required value not provided in request"}), 500


class Terminate(MethodView):
    """
    Endpoint to stop the server on the robot.
    This will stop commands from being processed,
    however it will not stop tasks running on parallel controllers.
    """
    def post(self):
        shutdown = request.environ.get("werkzeug.server.shutdown")
        if shutdown is None:
            raise RuntimeError("Not running with the Werkzeug Server")
        shutdown()
