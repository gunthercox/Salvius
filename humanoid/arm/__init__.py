from flask.ext.restful import Resource
from flask.ext.restful import marshal, fields, request

from humanoid.arm.shoulder import Shoulder
from humanoid.arm.elbow import Elbow
from humanoid.arm.wrist import Wrist
from humanoid.arm.hand import Hand


class Arm(Resource):

    def __init__(self, uuid):
        self._shoulder = Shoulder(uuid)
        self._elbow = Elbow(uuid)
        self._wrist = Wrist(uuid)
        self._hand = Hand(uuid)

        self.id = uuid

        self.data = {}

        self.fields = {
            "id": fields.Integer,
            "href": fields.String,
            "shoulder": fields.Nested(self._shoulder.fields),
            "elbow": fields.Nested(self._elbow.fields),
            "wrist": fields.Nested(self._wrist.fields),
            "hand": fields.Nested(self._hand.fields)
        }

    def get(self, arm_id):
        from flask import current_app as app

        robot = app.config["ROBOT"]

        self.data["id"] = arm_id
        self.data["href"] = "/arms/" + str(arm_id) + "/"
        self.data["shoulder"] = dict(robot._arms[arm_id]._shoulder.get(arm_id))
        self.data["elbow"] = dict(robot._arms[arm_id]._elbow.get(arm_id))
        self.data["wrist"] = dict(robot._arms[arm_id]._wrist.get(arm_id))
        #self.data["hand"] = dict(robot._arms[arm_id]._hand.get(arm_id))

        return marshal(self.data, self.fields)

    def set_shoulder(self, shoulder):
        self._shoulder = shoulder

    def set_elbow(self, elbow):
        self._elbow = elbow

    def set_wrist(self, wrist):
        self._wrist = wrist

    def set_hand(self, hand):
        self._hand = hand

    @property
    def shoulder(self):
        return self._shoulder.get(self.id)

    @property
    def elbow(self):
        return self._elbow

    @property
    def wrist(self):
        return self._wrist

    @property
    def hand(self):
        return self._hand
