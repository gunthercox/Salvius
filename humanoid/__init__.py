from flask.ext.restful import Resource
from flask.ext.restful import marshal, fields


class Robot(Resource):

    def __init__(self):
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

        self.data["neck"] = robot.neck.get()
        self.data["torso"] = robot.torso.get()

        arm_output = []
        id_count = 0
        for arm in robot.arms:
            arm_output.append(arm.get(id_count))
            id_count += 1

        self.data["arms"] = arm_output

        leg_output = []
        id_count = 0
        for leg in robot._legs:
            leg_output.append(leg.get(id_count))
            id_count += 1

        self.data["legs"] = leg_output

        return marshal(self.data, self.fields)
