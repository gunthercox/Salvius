from marshmallow import Serializer, fields

from humanoid.neck import Neck
from humanoid.torso import Torso
from humanoid.arm import Arm, ArmSerializer
from humanoid.leg import Legs

from humanoid.arm.shoulder import Shoulder
from humanoid.arm.elbow import Elbow
from humanoid.arm.wrist import Wrist
from humanoid.arm.hand import Hand, Finger

from humanoid.robot import Robot as Future


class Robot(Future):

    def __init__(self):
        super(Robot, self).__init__()
        self.name = self.db.data(key="name")

        self._neck = Neck()
        self._torso = Torso()
        self._arms = []
        self._legs = Legs()

        # Create left arm
        left_arm = self.new_arm()

        left_shoulder = Shoulder()
        left_shoulder.set_parent_id(left_arm.id)
        left_arm.set_shoulder(left_shoulder)

        left_elbow = Elbow()
        left_elbow.set_parent_id(left_arm.id)
        left_arm.set_elbow(left_elbow)

        left_wrist = Wrist()
        left_wrist.set_parent_id(left_arm.id)
        left_arm.set_wrist(left_wrist)

        left_hand = Hand()
        left_hand.set_parent_id(left_arm.id)
        left_arm.set_hand(left_hand)

        left_thumb = Finger(hand_id=left_arm.id)
        for finger in range(4):
            left_hand.add_finger()

        left_hand.set_thumb(left_thumb)

        # Create right arm
        right_arm = self.new_arm()

        right_shoulder = Shoulder()
        right_shoulder.set_parent_id(right_arm.id)
        right_arm.set_shoulder(right_shoulder)

        right_elbow = Elbow()
        right_elbow.set_parent_id(right_arm.id)
        right_arm.set_elbow(right_elbow)

        right_wrist = Wrist()
        right_wrist.set_parent_id(right_arm.id)
        right_arm.set_wrist(right_wrist)

        right_hand = Hand()
        right_hand.set_parent_id(right_arm.id)
        right_arm.set_hand(right_hand)

        right_thumb = Finger(hand_id=right_arm.id)
        for finger in range(4):
            right_hand.add_finger()

        right_hand.set_thumb(right_thumb)

    def new_arm(self):
        """
        Adds an arm object to the body.
        Sets a unique id to reference the listed index of the arm object.
        """
        uuid = 0
        if self._arms:
            uuid = max(arm.id for arm in self._arms) + 1

        arm = Arm(uuid)
        self._arms.append(arm)
        return arm

    @property
    def neck(self):
        return self._neck.get()

    @property
    def arms(self):
        return self._arms

    @property
    def torso(self):
        return self._torso.get()

    @property
    def legs(self):
        legs = self._legs.get()["legs"]
        return legs


class ArmsSerializer(Serializer):
    arms = fields.Nested(ArmSerializer, many=True)


class RobotSerializer(Serializer):
    name = fields.String()
    neck = fields.Raw()
    torso = fields.Raw()
    arms = fields.Nested(ArmSerializer, many=True)
    legs = fields.Raw()
