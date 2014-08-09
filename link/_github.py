import settings
import urllib2
import base64
import json

from settings import GITHUB


def basic_auth(username, password):
    """
    Encode the username and password.
    Note: options for oauth2 authentication are available.
    """
    username = GITHUB["USERNAME"]
    password = GITHUB["PASSWORD"]
    return base64.encodestring('%s:%s' % (username, password)).replace('\n', '')    

def star_repo(repo_url, username, password):
    """
    PUT /user/starred/:owner/:repo
    """
    opener = urllib2.build_opener(urllib2.HTTPHandler)
    request = urllib2.Request(repo_url, data='')
    base64string = basic_auth(username, password)
    request.add_header("Authorization", "Basic %s" % base64string)
    request.add_header('Content-Type', 'application/json')
    request.get_method = lambda: 'PUT'
    url = opener.open(request)

def follow_user(user_url, username, password)
    """
    PUT /user/following/:username
    """
    opener = urllib2.build_opener(urllib2.HTTPHandler)
    request = urllib2.Request(repo_url, data='')
    base64string = basic_auth(username, password)
    request.add_header("Authorization", "Basic %s" % base64string)
    request.add_header('Content-Type', 'application/json')
    request.get_method = lambda: 'PUT'
    url = opener.open(request)

# Test repo
# repo = "https://api.github.com/user/starred/toastdriven/django-tastypie"
# star_repo(repo, settings.username, settings.password)
