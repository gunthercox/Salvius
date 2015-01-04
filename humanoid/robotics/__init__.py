from jsondb.db import Database
from chatterbot import ChatBot

from humanoid.torso import Torso
from humanoid.arm import Arm
from humanoid.leg import Leg

from humanoid.arm.hand import Finger


class Robot(object):

    def __init__(self):
        self.db = Database("settings.db")
        self.chatbot = ChatBot()

        self._torso = Torso()
        self._arms = []
        self._legs = []

        # Add legs
        for leg in self.db.data(key="legs"):
            leg_id = leg["leg"]["id"]
            self._legs.append(Leg(leg_id))

        # Add arms
        for arm in self.db.data(key="arms"):
            arm_id = arm["arm"]["id"]
            self._arms.append(Arm(arm_id))

        # Add fingers
        for arm in self.arms:
            arm.hand._fingers = [Finger(arm.id, 0), Finger(arm.id, 1), Finger(arm.id, 2), Finger(arm.id, 3)]

    @property
    def arms(self):
        return self._arms

    @property
    def torso(self):
        return self._torso

    @property
    def legs(self):
        return self._legs
