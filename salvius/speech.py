from zorg.adaptor import Adaptor
from zorg.driver import Driver
from multiprocessing import Queue
import speech_recognition
import subprocess


class SpeechRecognition(Adaptor):

    def __init__(self, options):
        super(SpeechRecognition, self).__init__(options)

        self.recognizer = speech_recognition.Recognizer()
        self.microphone = speech_recognition.Microphone()

        # Allow different speech recognition methods to be selected
        # See https://pypi.python.org/pypi/SpeechRecognition/
        self.recognizer_function = options.get(
            "recognizer_function", "recognize_sphinx"
        )

        self.queue = Queue(maxsize=7)

        self.stop_listening = None

    def connect(self):
        subprocess.call(["jack_control", "start"])

        # we only need to calibrate once, before we start listening
        with self.microphone as source:
            self.recognizer.adjust_for_ambient_noise(source)

        # start listening in the background (note that we
        # don't have to do this inside a `with` statement)
        self.stop_listening = self.recognizer.listen_in_background(
            self.microphone,
            self.callback
        )
        # `stop_listening` is now a function that,
        # when called, stops background listening

    def disconnect(self):
        if self.stop_listening:
            self.stop_listening()

        subprocess.call(["jack_control", "stop"])

    def callback(self, recognizer, audio):

        recognizer_function = getattr(recognizer, self.recognizer_function)

        # this is called from the background thread
        # received audio data, now we'll recognize it using speech recognition
        try:
            result = recognizer_function(audio)
            self.queue.put(result)
        except speech_recognition.UnknownValueError:
            self.queue.put("I am sorry, I could not understand that.")
        except speech_recognition.RequestError as e:
            m = "My speech recognition service has failed. {0}"
            self.queue.put(m.format(e))


class ApiDriver(Driver):

    def __init__(self, options, connection):
        super(ApiDriver, self).__init__(options, connection)

        self.commands += ["get_words"]

    def start(self):
        self.connection.connect()

    def stop(self):
        self.connection.disconnect()

    def get_words(self):
        if self.connection.queue.empty():
            return None
        return self.connection.queue.get()
