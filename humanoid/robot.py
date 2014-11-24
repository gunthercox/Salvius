from jsondb.db import Database
from chatterbot import ChatBot

from humanoid.neck import Neck
from humanoid.torso import Torso
from humanoid.arm import Arm
from humanoid.leg import Leg

from humanoid.arm.shoulder import Shoulder
from humanoid.arm.elbow import Elbow
from humanoid.arm.wrist import Wrist
from humanoid.arm.hand import Hand


class Robot(object):

    def __init__(self):
        self.db = Database("settings.db")
        self.chatbot = ChatBot()

        self._neck = Neck()
        self._torso = Torso()
        self._arms = []
        self._legs = []

        for leg in self.db.data(key="legs"):
            leg_id = leg["leg"]["id"]
            self._legs.append(Leg(leg_id))

        for leg in self.db.data(key="legs"):
            arm_id = leg["leg"]["id"]
            self._arms.append(Arm(arm_id))

        '''
        for finger in range(4):
            left_hand.add_finger()

        for finger in range(4):
            right_hand.add_finger()
        '''

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
        output = []
        id_count = 0
        for arm in self._arms:
            output.append(arm.get(id_count))
            id_count += 1
        return output

    @property
    def torso(self):
        return self._torso.get()

    @property
    def legs(self):
        output = []
        id_count = 0
        for leg in self._legs:
            output.append(leg.get(id_count))
            id_count += 1
        return output
