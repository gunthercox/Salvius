from twitter import OAuth, Twitter, TwitterError, TwitterHTTPError
import settings


debug = settings.DEBUG


class TwitterTemp(object):
    def __init__(self):
        from jsondb.db import Database

        self.authorize_url = None
        self.logout_url = None

    def tweet_to_friends():
        """    
        Tweet one random message to the next friend in a list every hour.
        The tweet will not be sent and will be printed to the console when in
        debug mode.
        """
        from time import time, sleep
        from random import choice

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

    def generate_activity_data():
        """
        Counts the activity frequency for each day of the week.
        """

        from twitter import TwitterStream

        timeline = t.statuses.user_timeline(count=500)
        daily_sum = {
            "Sun": 0,
            "Mon": 0,
            "Tue": 0,
            "Wed": 0,
            "Thu": 0,
            "Fri": 0,
            "Sat": 0,
        }

        for post in timeline:
            day = post["created_at"].split(" ")[0]
            daily_sum[day] += 1
            
        print(daily_sum)
