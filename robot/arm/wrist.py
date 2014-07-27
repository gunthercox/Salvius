from marshmallow import Serializer, fields
from robot.joints import Joint


class Wrist(Joint):

    def __init__(self):
        super(Wrist, self).__init__()
        self.roll = 0
        self.pitch = 0
        self.yaw = 0

        self.parent_id = None

    def set_parent_id(self, uuid):
        self.parent_id = uuid

    def rotate(self, degrees):
        """
        Takes a positive or negative number to rotate the wrist
        relative to its current position.
        """
        self.roll += degrees

    def tilt(self, degrees):
        """
        Tilts writs
        """
        self.pitch += degrees

    def lean(self, degrees):
        """
        Angles the wrist left or right.
        """
        self.yaw += degrees

    def reset(self):
        self.roll = 0
        self.pitch = 0
        self.yaw = 0

    def get_position(self):
        return [self.roll, self.pitch, self.yaw]


class WristSerializer(Serializer):
    roll = fields.Integer()
    pitch = fields.Integer()
    yaw = fields.Integer()

    href = fields.Method("get_url")

    def get_url(self, obj):
        return "/api/robot/body/arms/" + str(obj.parent_id) + "/wrist/"
