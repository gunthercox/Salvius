from flask.ext.restful import Resource
from flask.ext.restful import marshal, fields, request
from humanoid.joints import CompliantJoint


class Finger(CompliantJoint):

    def __init__(self, uuid=None, hand_id=None):
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

    def __init__(self, arm_id=None):
        super(Thumb, self).__init__()
        self.parent_id = arm_id

    def get(self, arm_id):
        from flask import url_for

        self.data["href"] = url_for("thumb", arm_id=arm_id)

        return marshal(self.data, self.fields)

    def patch(self, arm_id):
        data = request.get_json(force=True)

        self.validate_fields(data)

        for key in data.keys():
            self.data[key] = data[key]

        return marshal(self.data, self.fields), 201


class Hand(Resource):

    def __init__(self, arm_id=None, fingers=[]):
        super(Hand, self).__init__()
        from humanoid.arm.hand import Finger, Thumb

        self.parent_id = arm_id

        self._fingers = fingers
        self._thumb = Thumb(arm_id)

        self.fields = {
            "fingers": fields.List(fields.Raw()),
            "thumb": fields.Nested(self.thumb.fields)
        }

        self.data = {}

    def get(self, arm_id):
        from flask import current_app as app

        robot = app.config["ROBOT"]

        finger_output = []
        id_count = 0
        for finger in robot.arms[arm_id].hand.fingers:
            finger_output.append(finger.get(arm_id, id_count))
            id_count += 1

        self.data["fingers"] = finger_output
        self.data["thumb"] = dict(self.thumb.get(arm_id))

        return marshal(self.data, self.fields)

    @property
    def fingers(self):
        return self._fingers

    @property
    def thumb(self):
        return self._thumb
