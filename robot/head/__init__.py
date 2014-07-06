from marshmallow import Serializer, fields

class Head(object):

    def __init__(self):
        self.camera_url = ""

    def set_camera_url(self, url):
        self.camera_url = url

    def get_camera_url(self):
        return self.camera_url


class Neck(object):
    """
    The tilt of the robot's head is controlled by two
    motors (one on eiter side on the front of the neck).
    """

    def __init__(self):
        self.rotation = 0
        self.right_elevation = 0
        self.left_elevation = 0
        self._head = None

    def set_head(self, head):
        self._head = head

    @property
    def head(self):
        return self._head


class HeadSerializer(Serializer):
    camera_url = fields.String()


class NeckSerializer(Serializer):
    rotation = fields.Integer()
    right_elevation = fields.Integer()
    left_elevation = fields.Integer()
