import tweepy
from tweepy import TweepyException
from time import sleep
from dotenv import dotenv_values

from func import bot_tweet, logging

# Get client & api auth using v1
env = dotenv_values(".env")
client = tweepy.Client(
    bearer_token=env.get("BEARER_TOKEN"),
    consumer_key=env.get("API_KEY"),
    consumer_secret=env.get("API_KEY_SECRET"),
    access_token=env.get("ACCESS_TOKEN"),
    access_token_secret=env.get("ACCESS_TOKEN_SECRET")
)
auth = tweepy.OAuth1UserHandler(
    consumer_key=env.get("API_KEY"),
    consumer_secret=env.get("API_KEY_SECRET"),
    access_token=env.get("ACCESS_TOKEN"),
    access_token_secret=env.get("ACCESS_TOKEN_SECRET")
)
api = tweepy.API(auth)

# Tweet indefinitely every 30 mins
while True:
    try:
        bot_tweet.bot_tweet(bot_api=api, bot_client=client)
        sleep(30 * 60)

    # On exception, log error and execute appropriate time to wait
    except TweepyException as e:
        logging.log_error(e)
        sleep(60)

        flag = False
        # Check last tweet, loop until the fucking thing actually works
        while not flag:
            try:
                # If last tweet was less than 3 mins ago, sleep 30 mins (Tweet was sent despite exception)
                if bot_tweet.get_time_since_last_tweet(bot_client=client) < 3 * 60:
                    sleep(30 * 60)
                else:
                    sleep(30)
                # Trigger flag to stop loop
                flag = True
            # If exception when trying to get last tweet, wait 10 secs then try again
            except TweepyException as e:
                sleep(10)
