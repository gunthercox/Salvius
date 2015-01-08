from chatterbot import ChatBot
from flask import Flask

from humanoid import api as robot_api
from humanoid.views import Connect, TemplateView
from humanoid import social
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

# Create flask app
app = Flask(__name__, static_folder="static", static_url_path="")

app.add_url_rule("/", view_func=TemplateView.as_view("interface", template_name="interface.html"))
app.add_url_rule("/hands/", view_func=TemplateView.as_view("hands", template_name="hands.html"))
app.add_url_rule("/sensors/", view_func=TemplateView.as_view("sensors", template_name="sensors.html"))
app.add_url_rule("/communication/", view_func=TemplateView.as_view("communication", template_name="chat.html"))
app.add_url_rule("/health/", view_func=TemplateView.as_view("health", template_name="status.html"))
app.add_url_rule("/connect/", view_func=Connect.as_view("connect"))

app.add_url_rule("/twitter/authorized/", view_func=social.TwitterAuthorizedView.as_view("twitter_authorized"))
app.add_url_rule("/google/authorized/", view_func=social.GoogleAuthorizedView.as_view("google_authorized"))
app.add_url_rule("/disqus/authorized/", view_func=social.DisqusAuthorizedView.as_view("disqus_authorized"))
app.add_url_rule("/connect/twitter/", view_func=social.TwitterConnectView.as_view("connect_twitter"))
app.add_url_rule("/connect/google/", view_func=social.GoogleConnectView.as_view("connect_google"))
app.add_url_rule("/connect/disqus/", view_func=social.DisqusConnectView.as_view("connect_disqus"))
app.add_url_rule("/connect/github/", view_func=social.GitHubConnectView.as_view("connect_github"))

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

app.add_url_rule("/terminate/",view_func=robot_api.Terminate.as_view("terminate"))
app.add_url_rule("/speech/", view_func=robot_api.Speech.as_view("speech"))
app.add_url_rule("/writing/", view_func=robot_api.Writing.as_view("writing"))
app.add_url_rule("/chat/", view_func=robot_api.Chat.as_view("chat"))
app.add_url_rule("/api/status/", view_func=robot_api.Status.as_view("status"))

if __name__ == "__main__":
    app.config["GITHUB"] = None
    app.config["TWITTER"] = None
    app.config["GOOGLE"] = None
    app.config["DISQUS"] = None
    app.config["CHATBOT"] = ChatBot()
    app.config["DEBUG"] = True
    app.config["SECRET_KEY"] = "development"

    social.oauth.init_app(app)

    app.run(host="0.0.0.0", port=8000)
