from marshmallow import Serializer, fields


class Joint(object):
    """
    A base class with methods to be used by other joints.
    """

    def set_method(self, data):
        """
        A setter method which takes a dictionary as a parameter and
        calls setter methods prefixed with 'set_' if they exist.
        """

        # For each key-value pair in the dictionary
        for key in data.keys():
            method = "set_" + str(key)
            value = data[key]

            try:
                getattr(self, method)(value)
            except:
                raise Exception("Method %s not implemented" % method)


class HingeJoint(Joint):

    def __init__(self, angle=0):
        super(HingeJoint, self).__init__()
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

