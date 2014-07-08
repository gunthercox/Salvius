from unittest import TestCase
from flask import Flask, request

from robot import Robot, RobotSerializer
from robot.body import BodySerializer
from robot.arm import Arm, ArmSerializer
from robot.arm.shoulder import Shoulder, ShoulderSerializer
from robot.arm.elbow import Elbow, ElbowSerializer
from robot.arm.wrist import Wrist, WristSerializer
from robot.arm.hand import Hand, HandSerializer
from robot.arm.hand import Finger, FingerSerializer

class TestRenderTemplates(TestCase):

    def test_test(self):

        # I'm skipping this test for now because i'm not sure how to unit test an api
        return


        import json
        import urllib2

        app = Flask(__name__)
        app.config['TESTING'] = True

        #app.run(host='0.0.0.0', port=5000, debug=True)

        port = app.config.get('LIVESERVER_PORT', 5000)

        test_string = "Test text"
        url = 'http://localhost:%s/api/speech/' % port
        data = json.dumps({"speech_text": test_string})
        req = urllib2.Request(url, data, {'Content-Type': 'application/json'})
        response = urllib2.urlopen(req)

        data = response.read()
        response.close()

        self.assertTrue(test_string in data)

