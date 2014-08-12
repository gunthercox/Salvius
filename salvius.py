from flask import Flask
from flask.ext.restful import Api

from humanoid import views

from humanoid.neck import Neck
from humanoid.torso import Torso

from humanoid.leg import Legs, Leg

from humanoid.arm.shoulder import Shoulder
from humanoid.arm.elbow import Elbow
from humanoid.arm.wrist import Wrist
from humanoid.arm.hand import Finger
from humanoid.arm.hand import Thumb

from humanoid.leg.hip import Hip
from humanoid.leg.knee import Knee
from humanoid.leg.ankle import Ankle

from humanoid.speech import Speech
from humanoid.writing import Writing
from humanoid.settings import Settings


# Create flask app
app = Flask(__name__, static_folder="static", static_url_path="")
api = Api(app)

@app.route('/connect/github/')
def callback():
    """
    OAuth callback from GitHub
    """
    from flask import request, redirect
    from humanoid.views import get_token

    code = request.args.get("code", "")
    print("___THE TOKEN IS:___", get_token(code))

    return redirect('/connect/')


app.add_url_rule("/", view_func=views.App.as_view("app"))
app.add_url_rule("/connect/", view_func=views.Connect.as_view("connect"))

# Setup the Api resource routing
api.add_resource(views.ApiRobot, "/api/robot/")
api.add_resource(views.ApiBody, "/api/robot/body/")
api.add_resource(Neck, "/api/robot/body/neck/")
api.add_resource(Torso, "/api/robot/body/torso/")

api.add_resource(views.ApiArms, "/api/robot/body/arms/")
api.add_resource(views.ApiArm, "/api/robot/body/arms/<int:arm_id>/")
api.add_resource(Shoulder, "/api/robot/body/arms/<int:arm_id>/shoulder/")
api.add_resource(Elbow, "/api/robot/body/arms/<int:arm_id>/elbow/")
api.add_resource(Wrist, "/api/robot/body/arms/<int:arm_id>/wrist/")
api.add_resource(views.ApiHand, "/api/robot/body/arms/<int:arm_id>/hand/")
api.add_resource(views.ApiFingers, "/api/robot/body/arms/<int:arm_id>/hand/fingers/")
api.add_resource(Finger, "/api/robot/body/arms/<int:arm_id>/hand/fingers/<int:finger_id>/")
api.add_resource(Thumb, "/api/robot/body/arms/<int:arm_id>/hand/thumb/")

api.add_resource(Legs, "/api/robot/body/legs/")
api.add_resource(Leg, "/api/robot/body/legs/<int:leg_id>/")
api.add_resource(Hip, "/api/robot/body/legs/<int:leg_id>/hip/")
api.add_resource(Knee, "/api/robot/body/legs/<int:leg_id>/knee/")
api.add_resource(Ankle, "/api/robot/body/legs/<int:leg_id>/ankle/")

api.add_resource(views.Terminate, "/api/terminate/")
api.add_resource(Settings, "/api/settings/")
api.add_resource(Speech, "/api/speech/")
api.add_resource(Writing, "/api/writing/")

api.add_resource(views.ApiBase, "/api/")

if __name__ == "__main__":
    app.config.update(
        DEBUG=True,
        SECRET_KEY="development",
        JSON_SORT_KEYS=False
    )
    app.run(host="0.0.0.0", port=8000)
