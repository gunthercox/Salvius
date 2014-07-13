from marshmallow import Serializer, fields

from robot.body import Body, BodySerializer
from robot.arm.shoulder import Shoulder
from robot.arm.elbow import Elbow
from robot.arm.wrist import Wrist
from robot.arm.hand import Hand, Finger
from robot.leg.hip import Hip
from robot.leg.knee import Knee
from robot.leg.ankle import Ankle
from robot.leg.foot import Foot


class Robot(object):

    def __init__(self, name="", body=None):
        self.name = name
        self._body = body

        # Create a default humanoid robot if one is not passed in as a parameter
        if body is None:
            self._body = Body()

            # Create left arm
            left_arm = self.body.new_arm()

            left_shoulder = Shoulder()
            left_arm.set_shoulder(left_shoulder)

            leftElbow = Elbow()
            left_arm.set_elbow(leftElbow)

            left_wrist = Wrist()
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
            right_arm.set_shoulder(right_shoulder)

            leftElbow = Elbow()
            right_arm.set_elbow(leftElbow)

            right_wrist = Wrist()
            right_arm.set_wrist(right_wrist)

            right_hand = Hand()
            right_hand.set_parent_id(right_arm.id)
            right_arm.set_hand(right_hand)

            right_thumb = Finger(hand_id=right_arm.id)
            for finger in range(4):
                right_hand.add_finger()

            right_hand.set_thumb(right_thumb)

            # Create left leg
            left_leg = self.body.new_leg()

            right_hip = Hip()
            left_leg.set_hip(right_hip)

            left_knee = Knee()
            left_leg.set_knee(left_knee)

            right_ankle = Ankle()
            left_leg.set_ankle(right_ankle)

            right_foot = Foot()
            left_leg.set_foot(right_foot)

            # Create right leg
            right_leg = self.body.new_leg()

            right_hip = Hip()
            right_leg.set_hip(right_hip)

            right_knee = Knee()
            right_leg.set_knee(right_knee)

            right_ankle = Ankle()
            right_leg.set_ankle(right_ankle)

            right_foot = Foot()
            right_leg.set_foot(right_foot)
            

    @property
    def body(self):
        return self._body


class RobotSerializer(Serializer):
    name = fields.String()
    body = fields.Nested(BodySerializer)
