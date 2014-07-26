from unittest import TestCase
from robot.joints import Joint


class TestObject(Joint):
    """
    This is a test object for other tests
    to use. This object extends the `Joint`
    object which has setter methods used to
    deserialize data from patch requests to
    the robot's api.
    """

    def __init__(self):
        self.color = ""
        self.name = ""

    def set_color(self, value):
        self.color = value

    def set_name(self, value):
        self.name = value


class Tests(TestCase):

    def test_set_attribute(self):
        obj = TestObject()
        obj.set_attribute("color", "green")

        self.assertEqual(obj.color, "green")

    def test_set_attributes(self):
        obj = TestObject()
        obj.set_attributes({"color": "blue", "name": "Salvius"})

        self.assertEqual(obj.color, "blue")
        self.assertEqual(obj.name, "Salvius")

    def test_set_methods(self):
        obj = TestObject()
        obj.set_methods({"set_color": "orange", "set_name": "default"})

        self.assertEqual(obj.color, "orange")
        self.assertEqual(obj.name, "default")
