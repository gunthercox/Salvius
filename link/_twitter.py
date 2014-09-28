from twitter import OAuth, Twitter, TwitterError, TwitterHTTPError
import settings


debug = settings.DEBUG


def favorite(tweet):
    try:
        result = t.favorites.create(_id=tweet['id'])
        print "Favorited: %s, %s" % (result['text'], result['id'])
        return result
    except TwitterHTTPError as e:
        print "Error: ", e
        return None

def follow(username):
    try:
        result = t.friendships.create(screen_name=username)
        print "Friended: %s" % (username)
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
