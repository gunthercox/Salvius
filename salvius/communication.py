from zorg.adaptor import Adaptor
from zorg.driver import Driver
from chatterbot import ChatBot


class Conversation(Adaptor):

    def __init__(self, options):
        super(Conversation, self).__init__(options)

        if 'logic_adapters' not in options:
            options["logic_adapters"] = [
                "chatterbot.adapters.logic.ClosestMatchAdapter",
                "chatterbot.adapters.logic.EvaluateMathematically",
                "chatterbot.adapters.logic.TimeLogicAdapter"
            ]

        self.chatbot = ChatBot("Salvius", **options)

        self.chatbot.train(
            "chatterbot.corpus.english"
        )

    def respond(self, text):
        return self.chatbot.get_response(text)


class ApiDriver(Driver):

    def __init__(self, options, connection):
        super(ApiDriver, self).__init__(options, connection)

        self.commands += [
            "get_response",
        ]

    def get_response(self, text):
        return self.connection.respond(text)
