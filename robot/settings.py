from flask.ext.restful import Resource, request
import json


class Settings(Resource):

    def __init__(self):
        super(Settings, self).__init__()

        self.db = "settings.db"

    def get(self):
        db = open(self.db, "r")
        content = db.read()
        obj = json.loads(content)
        db.close()

        return obj

    def patch(self):
        json_data = request.get_json(force=True)

        db = open(self.db, "r")
        content = db.read()

        obj = json.loads(content)

        for key in json_data:
            obj[key] = json_data[key]

        db.close()

        with open(self.db, "w") as settings:
            json.dump(obj, settings)

        return obj, 201

    def put(self):
        json_data = request.get_json(force=True)

        with open(self.db, "w") as settings:
            json.dump(json_data, settings)

        return json_data, 201
