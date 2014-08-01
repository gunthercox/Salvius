from flask.ext.restful import Resource, request
from jsondb.db import Database


class Settings(Resource):

    def __init__(self):
        super(Settings, self).__init__()
        self.db = Database("settings.db")

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
