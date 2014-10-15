from flask.views import View
from flask.ext.restful import Resource
from flask import request, jsonify
#from chatterbot import ChatBot


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
        json_data = request.get_json(force=True)
        key = u'text'

        data = {}

        if key in json_data:
            data["input"] = json_data[key]
            data["response"] = "blah"

        return jsonify(data)
