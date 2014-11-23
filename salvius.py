from flask import Flask
from flask.ext.restful import Api

from humanoid import api as robot_api
from humanoid import views
from humanoid import social
from humanoid.neck import Neck
from humanoid.torso import Torso
from humanoid.arm.shoulder import Shoulder
from humanoid.arm.elbow import Elbow
from humanoid.arm.wrist import Wrist
from humanoid.arm.hand import Finger
from humanoid.arm.hand import Thumb
from humanoid.leg import Legs, Leg
from humanoid.leg.hip import Hip
from humanoid.leg.knee import Knee
from humanoid.leg.ankle import Ankle
from humanoid import Robot

try:
    import settings
except ImportError:
    pass

# Create flask app
app = Flask(__name__, static_folder="static", static_url_path="")
api = Api(app)

@app.route("/test/")
def get_tokens():
    # Delete this method later
    from flask import session
    cookie = str(dict(session))
    return cookie

app.add_url_rule("/interface/", view_func=views.App.as_view("app"))
app.add_url_rule("/limbs/", view_func=views.Limbs.as_view("limbs"))
app.add_url_rule("/connect/", view_func=views.Connect.as_view("connect"))
app.add_url_rule("/chat/", view_func=views.Chat.as_view("communication"))
app.add_url_rule("/sensors/", view_func=views.Sensors.as_view("sensors"))
app.add_url_rule("/configuration/", view_func=views.Settings.as_view("setting"))

app.add_url_rule("/twitter/authorized/", view_func=social.TwitterAuthorizedView.as_view("twitter_authorized"))
app.add_url_rule("/google/authorized/", view_func=social.GoogleAuthorizedView.as_view("google_authorized"))
app.add_url_rule("/disqus/authorized/", view_func=social.DisqusAuthorizedView.as_view("disqus_authorized"))
app.add_url_rule("/connect/twitter/", view_func=social.TwitterConnectView.as_view("connect_twitter"))
app.add_url_rule("/connect/google/", view_func=social.GoogleConnectView.as_view("connect_google"))
app.add_url_rule("/connect/disqus/", view_func=social.DisqusConnectView.as_view("connect_disqus"))
app.add_url_rule("/connect/github/", view_func=social.GitHubConnectView.as_view("connect_github"))

api.add_resource(robot_api.Base, "/")
api.add_resource(Neck, "/neck/")
api.add_resource(Torso, "/torso/")

api.add_resource(robot_api.Arms, "/arms/")
api.add_resource(robot_api.Arm, "/arms/<int:arm_id>/")
api.add_resource(Shoulder, "/arms/<int:arm_id>/shoulder/")
api.add_resource(Elbow, "/arms/<int:arm_id>/elbow/")
api.add_resource(Wrist, "/arms/<int:arm_id>/wrist/")
api.add_resource(robot_api.Hand, "/arms/<int:arm_id>/hand/")
api.add_resource(robot_api.Fingers, "/arms/<int:arm_id>/hand/fingers/")
api.add_resource(Finger, "/arms/<int:arm_id>/hand/fingers/<int:finger_id>/")
api.add_resource(Thumb, "/arms/<int:arm_id>/hand/thumb/")

api.add_resource(Legs, "/legs/")
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
    app.config.update(
        DEBUG=True,
        SECRET_KEY="development",
        JSON_SORT_KEYS=False
    )
    app.config["ROBOT"] = Robot()
    app.config["GITHUB"] = settings.GITHUB
    app.config["TWITTER"] = settings.TWITTER
    app.config["GOOGLE"] = settings.GOOGLE
    app.config["DISQUS"] = settings.DISQUS
    app.config["PHANT"] = settings.PHANT

    social.oauth.init_app(app)

    app.run(host="0.0.0.0", port=8000)
