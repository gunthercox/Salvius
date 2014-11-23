from unittest import TestCase
import salvius


class Test(TestCase):

    def setUp(self):
        salvius.app.config["TESTING"] = True
        self.app = salvius.app.test_client()

    def test_speech(self):
        data = '{"speech_text": "Testing robot speech"}'

        response = self.app.post("/speech/", data=data, content_type="application/json")

        self.assertTrue("Testing robot speech" in response.data.decode())
