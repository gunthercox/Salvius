from marshmallow import Serializer, fields
from ..arm import ArmSerializer

class Body(object):

    def __init__(self):
        self.head = None
        self.arms = []
        self.legs = []

    def addHead(self, head):
        self.head.append(head)

    def addArm(self, arm):
        self.arms.append(arm)

    def addLegs(self, leg):
        self.legs.append(leg)

    def list_arms(self):
        return self.arms

class BodySerializer(Serializer):
    arms = fields.Nested(ArmSerializer, many=True)
