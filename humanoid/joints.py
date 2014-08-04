from flask.ext.restful import Resource
from flask.ext.restful import marshal, fields, request

# Marshmallow may be depricated in the future
from marshmallow import Serializer
from marshmallow import fields as lame


class Joint(Resource):
    """
    Represents a joint which permits rotation in two directions
    Body-joint examples: Torso
    """

    def __init__(self, joint_type):
        super(Joint, self).__init__()
        self.data = {}
        self.data["joint_type"] = joint_type

        self.fields = {
            "joint_type": fields.String,
            "href": fields.String
        }

        # Fields that can be modified through requests
        self.allowed_fields = []

    def validate_fields(self, data):
        from flask import abort
        for key in data.keys():
            if key not in self.allowed_fields:
                abort(405)

    @property
    def joint_type(self):
        return self.data["joint_type"]

    @property
    def href(self):
        return self.data["href"]

    def get(self):
        return marshal(self.data, self.fields)

    def patch(self):
        data = request.get_json(force=True)

        self.validate_fields(data)

        for key in data.keys():
            self.data[key] = data[key]

        return marshal(self.data, self.fields), 201


class HingeJoint(Joint):
    """
    Represents a joint in which the articular surfaces are molded to
    each other in such the manner as to permit motion only in one plane.
    Body-joint examples: Knees, Elbows, Phalanges
    """

    def __init__(self, angle=0):
        super(HingeJoint, self).__init__(joint_type="hinge")
        self.data["angle"] = angle

        self.fields["angle"] = fields.Integer
        self.fields["limits"] = fields.List(fields.Integer)

        self.allowed_fields.append("angle")

    def move(self, degrees):
        """
        Moves the joint relative to its current position.
        # TODO: Possible removal of all reset and move classes
        """
        self.data["angle"] += degrees

    @property
    def limits(self):
        return self.data["limits"]

    @property
    def angle(self):
        return self.data["angle"]


class PivotJoint(Joint):
    """
    Represents a joint which permits rotation in two directions.
    Body-joint examples: Torso 
    """

    def __init__(self, rotation=0):
        super(PivotJoint, self).__init__(joint_type="pivot")
        self.data["rotation"] = rotation

        self.fields["rotation"] = fields.Integer

        self.allowed_fields.append("rotation")

    def rotate(self, degrees):
        """
        Rotates the joint relative to its current position.
        """
        print(self.data)
        self.data["rotation"] += degrees

    @property
    def rotation(self):
        return self.data["rotation"]


class OrthogonalJoint(Joint):
    """
    Represents a joint which permits movement on one plane.
    This joint allows rotation on its axis.
    Body-joint examples: Shoulder, Hip
    """

    def __init__(self, rotation=0, angle=0):
        super(OrthogonalJoint, self).__init__(joint_type="orthogonal")
        self.data["rotation"] = rotation
        self.data["angle"] = angle

        self.fields["rotation"] = fields.Integer
        self.fields["angle"] = fields.Integer

        self.allowed_fields.append("rotation")
        self.allowed_fields.append("angle")

    def rotate(self, degrees):
        """
        Rotates the joint relative to its current position.
        """
        self.data["rotation"] += degrees

    def slant(self, degrees):
        """
        Angles the joint left or right relative to its current position.
        """
        self.data["angle"] += degrees

    @property
    def rotation(self):
        return self.data["rotation"]

    @property
    def angle(self):
        return self.data["angle"]


class ArticulatedJoint(Joint):
    """
    Represents a joint which permits movement on two planes as well
    as being able to rotate
    Body-joint examples: Wrist, Ankles
    """

    def __init__(self, rotation=0, elevation=0, angle=0):
        super(ArticulatedJoint, self).__init__(joint_type="articulated")
        self.data["rotation"] = rotation
        self.data["elevation"] = elevation
        self.data["angle"] = angle

        self.fields["rotation"] = fields.Integer
        self.fields["elevation"] = fields.Integer
        self.fields["angle"] = fields.Integer

        self.allowed_fields.append("rotation")
        self.allowed_fields.append("elevation")
        self.allowed_fields.append("angle")

    def rotate(self, degrees):
        """
        Rotates the joint relative to its current position.
        """
        self.data["rotation"] += degrees

    def elevate(self, degrees):
        """
        Raises or lowers the joint relative to its current position.
        """
        self.data["elevation"] += degrees

    def slant(self, degrees):
        """
        Angles the joint left or right relative to its current position.
        """
        self.data["angle"] += degrees

    @property
    def rotation(self):
        return self.data["rotation"]

    @property
    def elevation(self):
        return self.data["elevation"]

    @property
    def angle(self):
        return self.data["angle"]


class CompliantJoint(Joint):
    """
    The compliant joint type represents a body-joint structure where there are
    several joints linked together which will change shape based on the objects
    that the effector encounters.
    Body-joint example: Fingers
    """

    def __init__(self, tension=0):
        super(CompliantJoint, self).__init__(joint_type="compliant")
        self.data["tension"] = tension

        self.fields["tension"] = fields.Integer

        self.allowed_fields.append("tension")

    def move(self, degrees):
        """
        Moves the joint relative to its current position.
        """
        self.data["tension"] += degrees

    @property
    def tension(self):
        """
        Angles the joint left or right relative to its current position.
        """
        return self.data["tension"]

    @property
    def rotation(self):
        return self.data["rotation"]


class JointSerializer(Serializer):
    joint_type = lame.String()
    href = lame.String()


class HingeJointSerializer(JointSerializer):
    angle = lame.Integer()
    limits = lame.List(lame.Integer, attribute="limits")


class PivotJointSerializer(JointSerializer):
    rotation = lame.Integer()


class OrthogonalJointSerializer(JointSerializer):
    rotation = lame.Integer()
    angle = lame.Integer()


class ArticulatedJointSerializer(JointSerializer):
    rotation = lame.Integer()
    elevation = lame.Integer()
    angle = lame.Integer()


class CompliantJointSerializer(JointSerializer):
    tension = lame.Integer()
