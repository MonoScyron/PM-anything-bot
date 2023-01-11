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

    # On exception, log error, wait 30 seconds and try again
    except TweepyException as e:
        logging.log_error(e)
        sleep(30)
