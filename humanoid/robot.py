from flask.ext.restful import Resource
from jsondb.db import Database

class Robot(Resource):

    def __init__(self):
        super(Robot, self).__init__()
        self.db = Database("settings.db")
