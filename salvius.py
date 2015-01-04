from flask import Flask
from flask.ext.restful import Api

from humanoid import api as robot_api
from humanoid.views import Connect, TemplateView
from humanoid import social
from humanoid.neck import Neck
from humanoid.torso import Torso
from humanoid.arm import Arm
from humanoid.arm.shoulder import Shoulder
from humanoid.arm.elbow import Elbow
from humanoid.arm.wrist import Wrist
from humanoid.arm.hand import Hand
from humanoid.arm.hand import Finger
from humanoid.arm.hand import Thumb
from humanoid.leg import Leg
from humanoid.leg.hip import Hip
from humanoid.leg.knee import Knee
from humanoid.leg.ankle import Ankle

from humanoid import Robot as ApiRobot
from humanoid.robotics import Robot

try:
    import settings
except ImportError:
    pass

# Create flask app
app = Flask(__name__, static_folder="static", static_url_path="")
api = Api(app)

app.add_url_rule("/interface/", view_func=TemplateView.as_view("interface", template_name="interface.html"))
app.add_url_rule("/hands/", view_func=TemplateView.as_view("hands", template_name="hands.html"))
app.add_url_rule("/limbs/", view_func=TemplateView.as_view("limbs", template_name="limbs.html"))
app.add_url_rule("/sensors/", view_func=TemplateView.as_view("sensors", template_name="sensors.html"))
app.add_url_rule("/chat/", view_func=TemplateView.as_view("communication", template_name="chat.html"))
app.add_url_rule("/configuration/", view_func=TemplateView.as_view("configuration", template_name="settings.html"))
app.add_url_rule("/connect/", view_func=Connect.as_view("connect"))

app.add_url_rule("/twitter/authorized/", view_func=social.TwitterAuthorizedView.as_view("twitter_authorized"))
app.add_url_rule("/google/authorized/", view_func=social.GoogleAuthorizedView.as_view("google_authorized"))
app.add_url_rule("/disqus/authorized/", view_func=social.DisqusAuthorizedView.as_view("disqus_authorized"))
app.add_url_rule("/connect/twitter/", view_func=social.TwitterConnectView.as_view("connect_twitter"))
app.add_url_rule("/connect/google/", view_func=social.GoogleConnectView.as_view("connect_google"))
app.add_url_rule("/connect/disqus/", view_func=social.DisqusConnectView.as_view("connect_disqus"))
app.add_url_rule("/connect/github/", view_func=social.GitHubConnectView.as_view("connect_github"))

api.add_resource(ApiRobot, "/", endpoint="api")
api.add_resource(Neck, "/neck/")
api.add_resource(Torso, "/torso/")

api.add_resource(Arm, "/arms/<int:arm_id>/", endpoint="arms")
api.add_resource(Shoulder, "/arms/<int:arm_id>/shoulder/")
api.add_resource(Elbow, "/arms/<int:arm_id>/elbow/", endpoint="elbow")
api.add_resource(Wrist, "/arms/<int:arm_id>/wrist/")
api.add_resource(Hand, "/arms/<int:arm_id>/hand/")
api.add_resource(Finger, "/arms/<int:arm_id>/hand/fingers/<int:finger_id>/", endpoint="finger")
api.add_resource(Thumb, "/arms/<int:arm_id>/hand/thumb/", endpoint="thumb")

api.add_resource(Leg, "/legs/<int:leg_id>/")
api.add_resource(Hip, "/legs/<int:leg_id>/hip/")
api.add_resource(Knee, "/legs/<int:leg_id>/knee/")
api.add_resource(Ankle, "/legs/<int:leg_id>/ankle/")

api.add_resource(robot_api.Terminate, "/terminate/")
api.add_resource(robot_api.Settings, "/settings/")
api.add_resource(robot_api.Speech, "/speech/")
api.add_resource(robot_api.Writing, "/writing/")
api.add_resource(robot_api.Chat, "/chat/")

if __name__ == "__main__":
    app.config["GITHUB"] = settings.GITHUB
    app.config["TWITTER"] = settings.TWITTER
    app.config["GOOGLE"] = settings.GOOGLE
    app.config["DISQUS"] = settings.DISQUS
    app.config["PHANT"] = settings.PHANT
    app.config["ROBOT"] = Robot()
    app.config["DEBUG"] = True
    app.config["SECRET_KEY"] = "development"

    social.oauth.init_app(app)

    app.run(host="0.0.0.0", port=8000)
