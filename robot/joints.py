from marshmallow import Serializer, fields

class HingeJoint(object):

    def __init__(self, angle=0):
        self.angle = angle

    def move(self, degrees):
        """
        Moves the joint relative to its current position.
        """
        self.angle += degrees

    def reset(self):
        """
        Zeros the joints current position.
        """
        self.angle = 0

    def get_angle(self):
        return self.angle

class HingeJointSerializer(Serializer):
    angle = fields.Integer()
