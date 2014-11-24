from flask.ext.restful import Resource
from flask.ext.restful import marshal, fields, request

from humanoid.joints import CompliantJoint


class Finger(CompliantJoint):

    def __init__(self, uuid, hand_id):
        super(Finger, self).__init__()
        self.parent_id = hand_id
        self.id = uuid

        self.data["href"] = "/arms/" + str(self.parent_id) + "/hand/fingers/" + str(self.id)

    def get(self, arm_id, finger_id):
        from flask import url_for
        self.data["href"] = url_for("finger", arm_id=arm_id, finger_id=finger_id)
        return marshal(self.data, self.fields)

    def patch(self, arm_id, finger_id):
        data = request.get_json(force=True)

        self.validate_fields(data)

        for key in data.keys():
            self.data[key] = data[key]

        return marshal(self.data, self.fields), 201


class Thumb(CompliantJoint):
    """
    Thumbs work very similar to fingers, however they have other attributes
    which allow them to be opposable.
    """

    def __init__(self, arm_id):
        super(Thumb, self).__init__()
        self.parent_id = arm_id

    def get(self, arm_id):
        from flask import url_for

        self.data["href"] = url_for("thumb", arm_id=arm_id)
        self.data["href"] = "/arms/" + str(self.parent_id) + "/hand/thumb/"

        return marshal(self.data, self.fields)

    def patch(self, arm_id):
        data = request.get_json(force=True)

        self.validate_fields(data)

        for key in data.keys():
            self.data[key] = data[key]

        return marshal(self.data, self.fields), 201


class Hand(Resource):

    def __init__(self, arm_id):
        super(Hand, self).__init__()
        from humanoid.arm.hand import Thumb

        self.parent_id = arm_id

        self._fingers = []
        self._thumb = Thumb(arm_id)

        self.fields = {
            #"fingers": fields.Nested(self._fingers.fields),
            "thumb": fields.Nested(self._thumb.fields)
        }

        self.data = {}

    def get(self, arm_id):
        from flask import current_app as app

        robot = app.config["ROBOT"]
        self.data["thumb"] = dict(robot._arms[arm_id]._hand._thumb.get(arm_id))

        return marshal(self.data, self.fields)

    def add_finger(self):
        """
        Adds a finger to the hand.
        Sets a unique id to reference the listed index of the object.
        """
        uuid = 0
        if self._fingers:
            uuid = max(finger.id for finger in self._fingers) + 1

        finger = Finger(uuid, self.parent_id)
        self._fingers.append(finger)

    @property
    def fingers(self):
        return self._fingers

    @property
    def thumb(self):
        return self._thumb
