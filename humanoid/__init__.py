from flask.ext.restful import Resource
from flask.ext.restful import marshal, fields


class Robot(Resource):

    def __init__(self):
        super(Robot, self).__init__()

        self.fields = {
            "neck": fields.Raw(),
            "torso": fields.Raw(),
            "arms": fields.List(fields.Raw()),
            "legs": fields.List(fields.Raw())
        }

        self.data = {}

    def get(self):
        from flask import current_app as app
        robot = app.config["ROBOT"]

        self.data["neck"] = robot.neck
        self.data["torso"] = robot.torso
        self.data["arms"] = robot.arms
        self.data["legs"] = robot.legs

        return marshal(self.data, self.fields)
