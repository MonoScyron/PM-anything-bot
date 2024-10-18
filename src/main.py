import threading
import tweepy

from dotenv import dotenv_values
from mastodon import Mastodon
from atproto import Client

import bot
import eventparser

env = dotenv_values('.env')

bsky_client = Client('https://bsky.social')
bsky_client.login(env.get('BSKY_USERNAME'), env.get('BSKY_PASSWORD'))

mstdn_client = Mastodon(
    access_token=env.get("MSTDN_ACCESS_TOKEN"),
    api_base_url='https://mastodon.social'
)

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

parser = eventparser.EventParser()
parsed_text, pics = parser.parse_event()

twt_thread = threading.Thread(target=bot.twt_post(twt_api=twt_api,
                                                  twt_client=twt_client,
                                                  parsed_text=parsed_text,
                                                  pics=pics))
mstdn_thread = threading.Thread(target=bot.mstdn_post(mstdn_client=mstdn_client, parsed_text=parsed_text, pics=pics))
bsky_thread = threading.Thread(target=bot.bsky_post(bsky_client=bsky_client, parsed_text=parsed_text, pics=pics))

twt_thread.start()
mstdn_thread.start()
bsky_thread.start()

twt_thread.join()
mstdn_thread.join()
bsky_thread.join()
