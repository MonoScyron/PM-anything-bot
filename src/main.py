import sys
import threading
from time import sleep

import tweepy
from dotenv import dotenv_values
from mastodon import Mastodon

import bot
import eventparser

env = dotenv_values(".env")

mstdn_client = Mastodon(
    access_token=env.get("MSTDN_ACCESS_TOKEN"),
    api_base_url='https://mastodon.social'
)

# * Twitter
twt_client = tweepy.Client(
    bearer_token=env.get("TWITTER_BEARER_TOKEN"),
    consumer_key=env.get("TWITTER_API_KEY"),
    consumer_secret=env.get("TWITTER_API_KEY_SECRET"),
    access_token=env.get("TWITTER_ACCESS_TOKEN"),
    access_token_secret=env.get("TWITTER_ACCESS_TOKEN_SECRET")
)
twt_auth = tweepy.OAuth1UserHandler(
    consumer_key=env.get("TWITTER_API_KEY"),
    consumer_secret=env.get("TWITTER_API_KEY_SECRET"),
    access_token=env.get("TWITTER_ACCESS_TOKEN"),
    access_token_secret=env.get("TWITTER_ACCESS_TOKEN_SECRET")
)
twt_api = tweepy.API(twt_auth)

# Get time to wait until next post
args = sys.argv
wait_arg = 0
if len(args) > 2:
    raise ValueError("Too many args")
elif len(args) == 2:
    wait_arg = int(args[1])

# Wait arg mins before posting
sleep(wait_arg * 60)

parser = eventparser.EventParser()

# Post indefinitely every 30 mins
while True:
    parsed_text, pics = parser.parse_event()

    twt_thread = threading.Thread(target=bot.twt_post(twt_api=twt_api, twt_client=twt_client, parsed_text=parsed_text,
                                                      pics=pics))
    mstdn_thread = threading.Thread(target=bot.mstdn_post(mstdn_client=mstdn_client, parsed_text=parsed_text,
                                                          pics=pics))
    twt_thread.start()
    mstdn_thread.start()
    twt_thread.join()
    mstdn_thread.join()

    sleep(30 * 60)
