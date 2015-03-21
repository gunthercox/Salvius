from flask import request
from flask.views import MethodView
from robotics.decorators import analytics


class Chat(MethodView):

    @analytics("api_response_time")
    def post(self):
        from flask import current_app as app
        from flask import jsonify

        json_data = request.get_json(force=True)
        key = u'text'

        chatbot = app.config['CHATBOT']
        data = {}

        if key in json_data:
            data["input"] = json_data[key]
            data["response"] = chatbot.get_response(json_data[key])

        return jsonify(data)


class Speech(MethodView):

    @analytics("api_response_time")
    def post(self):
        from flask import jsonify
        from robotics.arduino import Arduino

        json_data = request.get_json(force=True)
        speech_text = u'speech_text'

        if speech_text in json_data:
            data = json_data[speech_text]

            text_to_speech = Arduino("/dev/ttyUSB1")
            #print text_to_speech.list_device_ports()
            text_to_speech.write(data)

            return jsonify(json_data), 201

        return jsonify({"warning": "required value not provided in request"}), 500

    @analytics("api_response_time")
    def get(self):
        from flask import abort
        abort(405)


class Writing(MethodView):

    @analytics("api_response_time")
    def post(self):
        from flask import jsonify
        json_data = request.get_json(force=True)
        text = u'text'

        if text in json_data:
            data = json_data[text]

            print(data)
            #TODO: Handle motor control for hand writing text

            return jsonify(json_data), 201

        return jsonify({"warning": "required value not provided in request"}), 500


class Status(MethodView):

    def get_response_times(self, analytics_key):
        from jsondb.db import Database
        database = Database("settings.db")

        if not analytics_key in database:
            return []

        return database[analytics_key]

    def bytes2human(self, n):
        # http://code.activestate.com/recipes/578019
        # >>> bytes2human(10000)
        # '9.8K'
        # >>> bytes2human(100001221)
        # '95.4M'
        symbols = ('KB', 'MB', 'GB', 'TB', 'PB', 'EB', 'ZB', 'YB')
        prefix = {}
        for i, s in enumerate(symbols):
            prefix[s] = 1 << (i + 1) * 10
        for s in reversed(symbols):
            if n >= prefix[s]:
                value = float(n) / prefix[s]
                return '%.1f%s' % (value, s)
        return "%sB" % n

    @analytics("api_response_time")
    def get(self):
        from flask import jsonify
        import psutil
        from datetime import datetime

        data = {}

        disk_useage = psutil.disk_usage("/")
        disk_io_counters = psutil.disk_io_counters(perdisk=False)
        net_io_counters = psutil.net_io_counters(pernic=False)
        virtual_memory = psutil.virtual_memory()
        swap_memory = psutil.swap_memory()

        data["cpu_percent"] = psutil.cpu_percent(interval=1, percpu=True)
        data["boot_time"] = datetime.fromtimestamp(psutil.boot_time()).strftime('%Y-%m-%d %H:%M:%S')

        data["disk_useage"] = {}
        data["disk_useage"]["free"] = self.bytes2human(disk_useage.free)
        data["disk_useage"]["percent"] = disk_useage.percent
        data["disk_useage"]["total"] = self.bytes2human(disk_useage.total)
        data["disk_useage"]["used"] = self.bytes2human(disk_useage.used)

        data["disk_io_counters"] = {}
        data["disk_io_counters"]["read"] = disk_io_counters.read_bytes
        data["disk_io_counters"]["write"] = disk_io_counters.write_bytes
        data["disk_io_counters"]["read_mb"] = self.bytes2human(disk_io_counters.read_bytes)
        data["disk_io_counters"]["write_mb"] = self.bytes2human(disk_io_counters.write_bytes)
        data["disk_io_counters"]["read_time"] = disk_io_counters.read_time
        data["disk_io_counters"]["write_time"] = disk_io_counters.write_time
        data["disk_io_counters"]["write_count"] = disk_io_counters.write_count

        # net_io_counters also supports dropin, dropout, errout
        data["net_io_counters"] = {}
        data["net_io_counters"]["received"] = net_io_counters.bytes_recv
        data["net_io_counters"]["sent"] = net_io_counters.bytes_sent
        data["net_io_counters"]["received_mb"] = self.bytes2human(net_io_counters.bytes_recv)
        data["net_io_counters"]["sent_mb"] = self.bytes2human(net_io_counters.bytes_sent)
        data["net_io_counters"]["packets_recv"] = net_io_counters.packets_recv
        data["net_io_counters"]["packets_sent"] = net_io_counters.packets_sent

        # virtual_memory also supports active, available, buffers, cached, inactive
        data["virtual_memory"] = {}
        data["virtual_memory"]["free"] = self.bytes2human(virtual_memory.free)
        data["virtual_memory"]["percent"] = virtual_memory.percent
        data["virtual_memory"]["total"] = self.bytes2human(virtual_memory.total)
        data["virtual_memory"]["used"] = self.bytes2human(virtual_memory.used)

        # swap_memory also supports sin, sout
        data["swap_memory"] = {}
        data["swap_memory"]["free"] = self.bytes2human(swap_memory.free)
        data["swap_memory"]["percent"] = swap_memory.percent
        data["swap_memory"]["total"] = self.bytes2human(swap_memory.total)
        data["swap_memory"]["used"] = self.bytes2human(swap_memory.used)

        # API response times
        data["api_response_time"] = self.get_response_times("api_response_time")
        data["web_response_time"] = self.get_response_times("web_response_time")

        return jsonify(data)


class GitHubConnectView(MethodView):

    @analytics("api_response_time")
    def get(self):
        """
        OAuth callback from GitHub
        """
        from flask import flash, redirect
        from flask import current_app as app
        import requests

        if "logout" in request.args:
            app.config["DATABASE"].delete("github_user")
            app.config["DATABASE"].delete("github_token")
        else:
            code = request.args.get("code", "")

            data = {
                "client_id": app.config["GITHUB"].github["CLIENT_ID"],
                "client_secret": app.config["GITHUB"].github["CLIENT_SECRET"],
                "code": code
            }

            headers = {"Accept": "application/json"}

            response = requests.post("https://github.com/login/oauth/access_token",
                                     data=data, headers=headers)
            token_json = response.json()

            # Save the value in the database
            app.config["DATABASE"]["github_token"] = token_json["access_token"]

            # Save the username
            token = "token " + token_json["access_token"]
            user = requests.get("https://api.github.com/user", headers={"Authorization": token})
            app.config["DATABASE"]["github_user"] = user.json()["name"]

            flash("You connected to GitHub as %s" % user.json()["name"])

        return redirect("/connect/")


class TwitterAuthorizedView(MethodView):

    @analytics("api_response_time")
    def get(self):
        from flask import flash, redirect
        from flask import current_app as app
        import requests

        if "logout" in request.args:
            app.config["DATABASE"].delete("twitter_user")
            app.config["DATABASE"].delete("twitter_token")
        else:
            app.logger.debug(request.args)
            app.logger.debug(request)

            verifier = request.args["oauth_verifier"]

            twitter = app.config["TWITTER"]
            twitter.verify(verifier)
            '''
            if resp is None:
                flash("You denied the request to sign in.")
            else:
            '''
            app.config["DATABASE"]['twitter_token'] = (
                twitter.oauth_token,
                twitter.oauth_token_secret
            )
            username = twitter.get_name()
            app.config["DATABASE"]["twitter_user"] = username
            flash("You connected to Twitter as %s" % username)

        return redirect("/connect/")



class DevicePorts(MethodView):

    @analytics("api_response_time")
    def get(self):
        """
        Display a list of device ports for easy debugging.
        """
        from robotics.arduino import Arduino
        from flask import jsonify

        arduino = Arduino()

        data = arduino.list_device_ports()
        return jsonify({"results": data})

class Terminate(MethodView):
    """
    Endpoint to stop the server on the robot.
    This will stop commands from being processed,
    however it will not stop tasks running on parallel controllers.
    """
    def post(self):
        shutdown = request.environ.get("werkzeug.server.shutdown")
        if shutdown is None:
            raise RuntimeError("Not running with the Werkzeug Server")
        shutdown()
