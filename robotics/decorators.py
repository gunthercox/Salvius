from functools import wraps
from jsondb.db import Database

class analytics(object):

    def __init__(self, log_key):
        """
        Takes a string parameter that will be used as a
        key to store logged data under in the database.
        """
        self.database = Database("settings.db")
        self.start_time = 0
        self.log_key = log_key

    def before(self):
        import time
        self.start_time = time.time()

    def after(self):
        import time

        response_time = int((time.time() - self.start_time) * 1000)

        if not self.log_key in self.database:
            self.database[self.log_key] = []

        analytics = self.database[self.log_key]

        # Only record the last 5 requests
        if len(analytics) == 50:
            analytics.pop(0)

        analytics.append(response_time)

        self.database[self.log_key] = analytics

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
