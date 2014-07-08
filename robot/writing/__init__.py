from flask import request
from flask.ext.restful import reqparse, Resource

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
