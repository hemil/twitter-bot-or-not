import sys
import logging
import tweepy
from datetime import datetime, timedelta

__author__ = "hemil"

usage = '''Usage: python get_common_bot_followers.py "Narendra Modi" "Amit Shah"'''

logger = logging.getLogger()

try:
    user_one = sys.argv[1]
    users_two = sys.argv[2]
except IndexError:
    logger.error(usage)
    exit(1)

# authorization
# Insert your credentials here
consumer_key = ''
consumer_secret = ''
access_key = ''
access_secret = ''
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_key, access_secret)

api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True, retry_count=3, retry_delay=60)


def get_followers(api, user_name):
    users = []
    page_count = 0
    for i, user in enumerate(tweepy.Cursor(api.followers, screen_name=user_name, count=200).pages()):
        print 'Getting page {} for followers'.format(i)
        users += user
        return users    # temp. for dev
    return users


def is_human(api, user_id):
    try:
        user = api.get_user(user_id)
    except:
        logger.error("User 404. User ID: {user_id}".format(user_id=user_id))
        return False
    user_name = user.screen_name

    user_description = user.description

    followers_count = user.followers_count
    following_count = user.friends_count

    verified = user.verified

    profile_pic_url = user.profile_image_url_https
    created_at = user.created_at
    # in a human account opened a few hours ago, it's possible # tweets = 0 or description is empty or the profile pic
    # is default. so allowing the default values
    allowed_defaults_time = datetime.utcnow() - timedelta(days=1)

    tweet_count = user._json.get("statuses_count")

    is_profile_pic_default = "default" in profile_pic_url

    if "bot" in user_name.lower():
        return False

    if is_profile_pic_default and created_at < allowed_defaults_time:
        return False
    else:
        if tweet_count < 10 and created_at < allowed_defaults_time:
            return False

        # 0 Followers, High Probability that it's fake or very very new
        # followers can be difficult, give them a week
        if followers_count == 0 and created_at < allowed_defaults_time - timedelta(days=6):
            return False

        if followers_count != 0:
            following_followers_ratio = following_count / followers_count

            if following_followers_ratio > 15 and not verified:
                return False

        # if user_description == "":
        #     return False

    return True

one_followers = get_followers(api, user_one)
one_bots = []
for one_follower in one_followers:
    if not is_human(api, one_follower.id):
        print one_follower.screen_name
        one_bots.append(one_follower.screen_name)

two_followers = get_followers(api, users_two)
two_bots = []
for two_follower in two_followers:
    if not is_human(api, two_follower.id):
        print two_follower.screen_name
        two_bots.append(two_follower.screen_name)

one_bots = set(one_bots)
common_bots = [two_bot for two_bot in two_bots if two_bot in one_bots]
print common_bots
