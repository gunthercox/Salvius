from marshmallow import Serializer, fields


class Joint(object):
    """
    A base class with methods to be used by other joints.
    """

    def set_attribute(self, attribue, value):
        return setattr(self, attribue, value)

    def set_attributes(self, data):
        """
        A method which takes a dictionary as a parameter and
        sets attribute values with if they exist.
        """

        for attribue in data.keys():
            attribue = str(attribue)
            print(attribue, data[attribue])

            if hasattr(self, attribue):
                self.set_attribute(attribue, data[attribue])
            else:
                raise Exception("Attribue %s not found" % attribue)

    def set_methods(self, data):
        """
        A setter method which takes a dictionary as a parameter and
        calls methods if they exist. Only one parametery is can currently
        be passed into a method.
        """

        for key in data.keys():
            method = str(key)
            value = data[key]

            if callable(getattr(self, method)):
                getattr(self, method)(value)
            else:
                raise Exception("Method %s not implemented" % method)


class HingeJoint(Joint):

    def __init__(self, angle=0):
        super(HingeJoint, self).__init__()
        self.angle = angle
        self.joint_type = "hinge"

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
    joint_type = fields.String()

