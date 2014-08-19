import requests


class Disqus(object):

    def __init__(self):
        from jsondb.db import Database

        self.db = Database("settings.db")
        self.token_key = "disqus_access_token"
        self.is_authorized = self.db.data(key=self.token_key) is not None
        self.authorize_url = None

    def comment(self, discussion_url):
        """
        TODO
        https://disqus.com/api/docs/auth/
        """

    def follow_user(self, user_url):
        """
        TODO
        """
