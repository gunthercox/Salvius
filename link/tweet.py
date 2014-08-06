from twitter import OAuth, Twitter, TwitterError, TwitterHTTPError

from time import time, sleep
from random import choice

import settings


debug = settings.DEBUG

auth = OAuth(
    consumer_key=settings.TWITTER["CONSUMER_KEY"],
    consumer_secret=settings.TWITTER["CONSUMER_SECRET"],
    token=settings.TWITTER["TOKEN"],
    token_secret=settings.TWITTER["TOKEN_SECRET"]
)

t = Twitter(auth=auth)

# Get screen name of this account
user = t.account.verify_credentials()["screen_name"]

def tweet_to_friends():
    """    
    Tweet one random message to the next friend in a list every hour.
    The tweet will not be sent and will be printed to the console when in
    debug mode.
    """

    # Get the list of robots
    robots = t.lists.members(owner_screen_name=user, slug="Robots")["users"]

    for robot in robots:
        message = " " + choice(open("messages.txt").readlines())
        msg = ("@" + robot["screen_name"] + message).strip("\n")

        if debug is True:
            print(msg)
        else:
            sleep(3600-time() % 3600)
            t.statuses.update(status=msg)

def get_mentions(mentioned):
    """
    Search for the latest tweets about someone
    """
    mentions = []
    x = t.search.tweets(q=mentioned)

    for i in x["statuses"]:
        user = i["user"]["screen_name"]
        # if we are not the user who posted it
        if user != mentioned:
            mentions.append(i)

    return mentions

def favorite(tweet):
    try:
        result = t.favorites.create(_id=tweet['id'])
        print "Favorited: %s, %s" % (result['text'], result['id'])
        return result
    except TwitterHTTPError as e:
        print "Error: ", e
        return None

def follow(user_name):
    try:
        result = t.friendships.create(screen_name=user_name)
        print "Friended: %s" % (user_name)
        return result
    except TwitterError as e:
        print "Error: ", e
        return None

def run():
    """
    Runs a check for twitter mentions.
    We will follow the user who mentioned us and
    favorite the post in which the mention was made.
    """
    mentions = get_mentions("SalviusRobot")

    for mention in mentions:
        user_name = mention["user"]["screen_name"]

        follow(user_name)
        favorite(mention)

