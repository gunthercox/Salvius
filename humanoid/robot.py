from flask.ext.restful import Resource
from jsondb.db import Database
from chatterbot import ChatBot

class Robot(Resource):

    def __init__(self):
        super(Robot, self).__init__()
        self.db = Database("settings.db")
        self.chatbot = ChatBot()
