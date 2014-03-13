from twitter import OAuth, Twitter
from time import time, sleep
from random import choice

import settings

auth = OAuth(
    consumer_key = settings.CONSUMER_KEY,
    consumer_secret = settings.CONSUMER_SECRET,
    token = settings.TOKEN,
    token_secret = settings.TOKEN_SECRET
)

t = Twitter(auth=auth)

# Get screen name of this account 
user = t.account.verify_credentials()["screen_name"]
    
# Get the list of robots
robots = t.lists.members(owner_screen_name=user, slug="Robots")["users"]

# Tweet one random message to the next robot every hour
for robot in robots:
    #sleep(3600-time()%3600)
    message = " " + choice(open("messages.txt").readlines())
    msg = ("@" + robot["screen_name"] + message).strip("\n")
    #t.statuses.update(status=msg)
    print(msg)
