from functools import wraps
from jsondb.db import Database

class analytics(object):

    def __init__(self):
        self.database = Database("settings.db")
        self.start_time = 0

    def before(self):
        import time
        self.start_time = time.time()

    def after(self):
        import time

        response_time = int((time.time() - self.start_time) * 1000)

        if not "api_response_time" in self.database:
            self.database["api_response_time"] = []

        analytics = self.database["api_response_time"]

        # Only record the last 5 requests
        if len(analytics) == 50:
            analytics.pop(0)

        analytics.append(response_time)

        self.database["api_response_time"] = analytics

    def __call__(self, wrappedCall):
        @wraps(wrappedCall)
        def wrapCall(*args, **kwargs):
            try:
                self.before()
                r = wrappedCall(*args, **kwargs)
            finally:
                self.after()
            return r
        return wrapCall
