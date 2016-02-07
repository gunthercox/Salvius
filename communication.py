from zorg.adaptor import Adaptor
from zorg.driver import Driver
from chatterbot import ChatBot


class Conversation(Adaptor):

    def __init__(self, options):
        super(Conversation, self).__init__(options)

        self.chatbot = ChatBot("Salvius", **options)

    def train_if_required(self):
        """
        Train the current chatterbot instance
        if it has not been trained yet.
        """
        # TODO


class ApiDriver(Driver):

    def __init__(self, options, connection):
        super(ApiDriver, self).__init__(options, connection)

        self.commands += [
            "get_response",
        ]

    def get_response(self, text):
        return self.connection.chatbot.get_response(text)

