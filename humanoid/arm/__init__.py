from flask.ext.restful import Resource
from flask.ext.restful import marshal, fields, request

from humanoid.arm.shoulder import Shoulder
from humanoid.arm.elbow import Elbow
from humanoid.arm.wrist import Wrist
from humanoid.arm.hand import Hand

from flask.views import MethodView


class Arm(MethodView):

    def __init__(self, uuid=None):
        self._shoulder = Shoulder(uuid)
        self._elbow = Elbow(uuid)
        self._wrist = Wrist(uuid)
        self._hand = Hand(uuid)

        self.id = uuid

        self.data = {}

        self.fields = {
            "id": fields.Integer,
            "href": fields.String,
            "shoulder": fields.Nested(self.shoulder.fields),
            "elbow": fields.Nested(self.elbow.fields),
            "wrist": fields.Nested(self.wrist.fields),
            "hand": fields.Nested(self.hand.fields)
        }

    def get(self, arm_id):
        from flask import current_app as app

        robot = app.config["ROBOT"]

        self.data["id"] = arm_id
        self.data["href"] = "/" + self.endpoint + "/" + str(arm_id) + "/"
        self.data["shoulder"] = dict(robot._arms[arm_id]._shoulder.get(arm_id))
        self.data["elbow"] = dict(robot.arms[arm_id].elbow.get(arm_id))
        self.data["wrist"] = dict(robot.arms[arm_id].wrist.get(arm_id))
        self.data["hand"] = dict(robot.arms[arm_id].hand.get(arm_id))

        return marshal(self.data, self.fields)

    @property
    def shoulder(self):
        return self._shoulder

    @property
    def elbow(self):
        return self._elbow

    @property
    def wrist(self):
        return self._wrist

    @property
    def hand(self):
        return self._hand
