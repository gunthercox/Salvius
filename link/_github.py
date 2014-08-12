import urllib2
import base64
import json

from settings import GITHUB


def basic_auth(username, password):
    """
    Encode the username and password.
    Note: options for oauth2 authentication are available.
    """
    return base64.encodestring('%s:%s' % (username, password)).replace('\n', '')

class GitHub(object):

    def __init__(self):
        from jsondb.db import Database

        self.db = Database("settings.db")
        self.token_key = "github_access_token"
        self.is_authorized = self.db.data(key=self.token_key) is not None
        self.authorize_url = None

    def star_repo(self, repo_url):
        """
        PUT /user/starred/:owner/:repo
        """
        import requests
        token = self.db.data(key=self.token_key)

        headers = {
            "Authorization": "token %s" % token,
            "Accept": "application/vnd.github.v3+json",
            "Content-Type": "application/json",
            "Content-Length": 0
        }

        response = requests.put(repo_url, headers=headers)

    def follow_user(self, user_url, username, password):
        """
        PUT /user/following/:username
        """
        opener = urllib2.build_opener(urllib2.HTTPHandler)
        request = urllib2.Request(repo_url, data='')
        auth = basic_auth(GITHUB["USERNAME"], GITHUB["PASSWORD"])
        request.add_header("Authorization", "Basic %s" % auth)
        request.add_header('Content-Type', 'application/json')
        request.get_method = lambda: 'PUT'
        url = opener.open(request)
