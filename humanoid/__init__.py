from marshmallow import Serializer, fields

from humanoid.body import Body, BodySerializer
from humanoid.arm.shoulder import Shoulder
from humanoid.arm.elbow import Elbow
from humanoid.arm.wrist import Wrist
from humanoid.arm.hand import Hand, Finger

from humanoid.robot import Robot as Future


class Robot(Future):

    def __init__(self):
        super(Robot, self).__init__()
        self.name = self.db.data(key="name")
        self.body = Body()

        # Create left arm
        left_arm = self.body.new_arm()

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
        right_arm = self.body.new_arm()

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


class RobotSerializer(Serializer):
    name = fields.String()
    body = fields.Nested(BodySerializer)
