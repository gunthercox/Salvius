from flask.views import View
from flask.ext.restful import Resource
from flask import request, jsonify


class Chat(View):

    def __init__(self):
        return super(Chat, self).__init__()

    def dispatch_request(self):
        from flask import render_template
        return render_template("chat.html")


class ChatApi(Resource):

    def __init__(self):
        return super(ChatApi, self).__init__()

    def post(self):
        from chatterbot import ChatBot

        json_data = request.get_json(force=True)
        key = u'text'

        chatbot = ChatBot()
        data = {}

        if key in json_data:
            data["input"] = json_data[key]
            data["response"] = chatbot.engram(json_data[key])

        return jsonify(data)
