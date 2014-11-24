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

    @property
    def neck(self):
        return self._neck

    @property
    def arms(self):
        return self._arms

    @property
    def torso(self):
        return self._torso

    @property
    def legs(self):
        return self._legs
