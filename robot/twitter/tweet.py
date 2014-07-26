from twitter import OAuth, Twitter
from time import time, sleep
from random import choice

import settings

debug = settings.DEBUG

auth = OAuth(
    consumer_key = settings.TWITTER["CONSUMER_KEY"],
    consumer_secret = settings.TWITTER["CONSUMER_SECRET"],
    token = settings.TWITTER["TOKEN"],
    token_secret = settings.TWITTER["TOKEN_SECRET"]
)

t = Twitter(auth=auth)

# Get screen name of this account 
user = t.account.verify_credentials()["screen_name"]
    
# Get the list of robots
robots = t.lists.members(owner_screen_name=user, slug="Robots")["users"]

# Tweet one random message to the next robot every hour if not in debug mode

for robot in robots:
    message = " " + choice(open("messages.txt").readlines())
    msg = ("@" + robot["screen_name"] + message).strip("\n")

    if debug == True:
        print(msg)
    else:
        sleep(3600-time() % 3600)
        t.statuses.update(status=msg)
