from flask.ext.restful import Resource
from flask.ext.restful import marshal, fields, request
from flask.ext.restful import fields as Fields

# Marshmallow may be depricated in the future
from marshmallow import Serializer
from marshmallow import fields as lame


class Joint(Resource):
    """
    Represents a joint which permits rotation in two directions
    Body-joint examples: Torso
    """

    def __init__(self):
        super(Joint, self).__init__()
        self.data = {}
        self.data["joint_type"] = "pivot"

        self.fields = {
            "joint_type": Fields.String,
            "href": Fields.String
        }

    @property
    def joint_type(self):
        return self.data["joint_type"]

    @property
    def href(self):
        return self.data["href"]

    def get(self):
        return marshal(self.data, self.fields)


class PivotJoint(Joint):
    """
    Represents a joint which permits rotation in two directions
    Body-joint examples: Torso
    """

    def __init__(self):
        super(PivotJoint, self).__init__()
        self.data["joint_type"] = "pivot"
        self.data["rotation"] = 0

        self.fields["rotation"] = Fields.Integer

    def rotate(self, degrees):
        """
        Rotates the joint relative to its current position.
        """
        print(self.data)
        self.data["rotation"] += degrees

    @property
    def rotation(self):
        return self.data["rotation"]


class Torso(PivotJoint):

    def __init__(self):
        super(Torso, self).__init__()
        self.data["href"] = "/api/robot/body/torso/"


class TorsoSerializer(Serializer):
    href = lame.String()
    rotation = lame.Integer()
    joint_type = lame.String()
