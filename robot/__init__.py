from marshmallow import Serializer, fields

from robot.body import Body, BodySerializer
from robot.arm import Arm
from robot.arm.shoulder import Shoulder
from robot.arm.elbow import Elbow
from robot.arm.wrist import Wrist
from robot.arm.hand import Hand, Finger


class Robot(object):

    def __init__(self, name=""):
        self._body = Body()
        self.name = name

    @property
    def body(self):
        return self._body

    def default(self):
        """
        Creates a basic humanoid robot
        """
        # Create left arm
        left_arm = Arm()
        self.body.add_arm(left_arm)

        left_shoulder = Shoulder()
        left_arm.set_shoulder(left_shoulder)

        leftElbow = Elbow()
        left_arm.set_elbow(leftElbow)

        left_wrist = Wrist()
        left_arm.set_wrist(left_wrist)

        left_hand = Hand()
        left_arm.set_hand(left_hand)

        left_thumb = Finger(0)
        for finger in range(4):
            left_hand.add_finger()

        left_hand.set_thumb(left_thumb)

        # Create right arm
        right_arm = Arm()
        self.body.add_arm(right_arm)

        right_shoulder = Shoulder()
        right_arm.set_shoulder(right_shoulder)

        leftElbow = Elbow()
        right_arm.set_elbow(leftElbow)

        right_wrist = Wrist()
        right_arm.set_wrist(right_wrist)

        right_hand = Hand()
        right_arm.set_hand(right_hand)

        right_thumb = Finger(0)
        for finger in range(4):
            right_hand.add_finger()

        right_hand.set_thumb(right_thumb)


class RobotSerializer(Serializer):
    name = fields.String()
    body = fields.Nested(BodySerializer)
