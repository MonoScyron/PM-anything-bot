import tweepy
import sys
from tweepy import TweepyException
from time import sleep
from dotenv import dotenv_values
from func import bot, logging

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

args = sys.argv
wait_arg = 0
if len(args) > 2:
    raise ValueError("Too many args")
elif len(args) == 2:
    wait_arg = int(args[1])

# Wait arg mins before tweeting
sleep(wait_arg * 60)

# Tweet indefinitely every 30 mins
while True:
    try:
        bot.bot_tweet(bot_api=api, bot_client=client)
        sleep(30 * 60)

    # On exception, log error and execute appropriate time to wait
    except TweepyException as e:
        logging.log_error(f'main.py - {e}')
        sleep(60)

        flag = False
        # Check last tweet, loop until the stupid thing actually works
        while not flag:
            try:
                # If last tweet was less than 3 mins ago, sleep 30 mins (Tweet was sent despite exception)
                if bot.get_time_since_last_tweet(bot_client=client) < 3 * 60:
                    sleep(30 * 60)
                else:
                    sleep(30)
                # Trigger flag to stop loop
                flag = True
            # If exception when trying to get last tweet, wait 10 secs then try again
            except TweepyException as e:
                sleep(10)
