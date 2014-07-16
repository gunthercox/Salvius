from flask import request

from flask.ext.restful import reqparse, Resource

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
