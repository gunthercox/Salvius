from chatterbot import ChatBot
from chatterbot.apis.twitter import Twitter
from chatterbot.apis.github import GitHub
from jsondb.db import Database
from flask import Flask

from humanoid import api
from humanoid.views import TemplateView, Connect
from humanoid.neck import Neck
from humanoid.torso import Torso
from humanoid.arm.shoulder import Shoulder
from humanoid.arm.elbow import Elbow
from humanoid.arm.wrist import Wrist
from humanoid.arm.hand import Finger
from humanoid.arm.hand import Thumb
from humanoid.leg.hip import Hip
from humanoid.leg.knee import Knee
from humanoid.leg.ankle import Ankle

settings_available = False

try:
    import settings
    settings_available = True
except ImportError:
    pass

# Create flask app
app = Flask(__name__, static_folder="static", static_url_path="")

app.add_url_rule("/", view_func=TemplateView.as_view("interface", template_name="interface.html"))

app.add_url_rule("/connect/", view_func=Connect.as_view("connect"))
app.add_url_rule("/connect/github/", view_func=api.GitHubConnectView.as_view("connect_github"))
app.add_url_rule("/connect/twitter/", view_func=api.TwitterAuthorizedView.as_view("connect_twitter"))

app.add_url_rule("/arms/<string:arm_name>/shoulder/", view_func=Shoulder.as_view("shoulder"))
app.add_url_rule("/arms/<string:arm_name>/elbow/", view_func=Elbow.as_view("elbow"))
app.add_url_rule("/arms/<string:arm_name>/wrist/", view_func=Wrist.as_view("wrist"))
app.add_url_rule("/arms/<string:arm_name>/finger/", view_func=Finger.as_view("finger"))
app.add_url_rule("/arms/<string:arm_name>/thumb/", view_func=Thumb.as_view("thumb"))

app.add_url_rule("/legs/<string:leg_name>/hip/", view_func=Hip.as_view("hip"))
app.add_url_rule("/legs/<string:leg_name>/knee/", view_func=Knee.as_view("knee"))
app.add_url_rule("/legs/<string:leg_name>/ankle/", view_func=Ankle.as_view("ankle"))

app.add_url_rule("/neck/", view_func=Neck.as_view("neck"))
app.add_url_rule("/torso/", view_func=Torso.as_view("torso"))

app.add_url_rule("/api/terminate/",view_func=api.Terminate.as_view("terminate"))
app.add_url_rule("/api/speech/", view_func=api.Speech.as_view("speech"))
app.add_url_rule("/api/writing/", view_func=api.Writing.as_view("writing"))
app.add_url_rule("/api/chat/", view_func=api.Chat.as_view("chat"))
app.add_url_rule("/api/status/", view_func=api.Status.as_view("status"))
app.add_url_rule("/api/device_ports/", view_func=api.DevicePorts.as_view("device_ports"))

if __name__ == "__main__":
    app.config["CHATBOT"] = ChatBot()
    app.config["DATABASE"] = Database("settings.db")
    app.config["DEBUG"] = True
    app.config["SECRET_KEY"] = "development"

    if settings_available:
        if hasattr(settings, "GITHUB"):
            app.config["GITHUB"] = GitHub(settings.GITHUB)
        if hasattr(settings, "TWITTER"):
            app.config["TWITTER"] = Twitter(settings.TWITTER)
        if hasattr(settings, "GOOGLE"):
            app.config["GOOGLE"] = settings.GOOGLE
        if hasattr(settings, "DISQUS"):
            app.config["DISQUS"] = settings.DISQUS

    app.run(host="0.0.0.0", port=8000)
