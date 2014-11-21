from flask.ext.restful import marshal, request
from marshmallow import Serializer, fields
from humanoid.joints import CompliantJoint, CompliantJointSerializer


class Finger(CompliantJoint):

    def __init__(self, uuid=None, hand_id=None):
        super(Finger, self).__init__()
        self.parent_id = hand_id
        self.id = uuid

        self.data["href"] = "/api/robot/body/arms/" + str(self.parent_id) + "/hand/fingers/" + str(self.id)

    def get(self, arm_id, finger_id):
        self.data["href"] = "/api/robot/body/arms/" + str(arm_id) + "/hand/fingers/" + str(finger_id)
        return marshal(self.data, self.fields)

    def patch(self, arm_id, finger_id):
        data = request.get_json(force=True)

        self.validate_fields(data)

        for key in data.keys():
            self.data[key] = data[key]

        return marshal(self.data, self.fields), 201


class Thumb(CompliantJoint):
    """
    Thumbs work very similar to fingers, however they have aditional attributes
    which allow them to be opposable.
    """

    def __init__(self, hand_id=None):
        super(Thumb, self).__init__()
        self.parent_id = hand_id

        self.data["href"] = "/api/arms/" + str(self.parent_id) + "/hand/thumb/"

    def get(self, arm_id):
        self.data["href"] = "/api/arms/" + str(arm_id) + "/hand/thumb/"
        return marshal(self.data, self.fields)

    def patch(self, arm_id):
        data = request.get_json(force=True)

        self.validate_fields(data)

        for key in data.keys():
            self.data[key] = data[key]

        return marshal(self.data, self.fields), 201


class Hand(object):

    def __init__(self):
        self._fingers = []
        self._thumb = None

        self.parent_id = None

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

    def set_parent_id(self, uuid):
        self.parent_id = uuid

    def set_thumb(self, thumb):
        """
        Takes a finger object as a parameter.
        """
        self._thumb = thumb

    @property
    def fingers(self):
        return self._fingers

    @property
    def thumb(self):
        return self._thumb


class FingerSerializer(CompliantJointSerializer):
    id = fields.UUID()
    position = fields.Integer()

    def get_url(self, obj):
        url = "/api/arms/" + str(obj.parent_id) + "/hand"

        # Only fingers should be created with an id
        if obj.id is not None:
            url += "/fingers/" + str(obj.id)
        else:
            url += "/thumb"

        return url


class FingersSerializer(Serializer):
    fingers = fields.Nested(FingerSerializer, many=True)


class HandSerializer(Serializer):
    fingers = fields.Nested(FingerSerializer, many=True)
    thumb = fields.Nested(FingerSerializer)
