import tweepy
import sys
from tweepy import TweepyException
from time import sleep
from dotenv import dotenv_values
from func import bot, logging, list_pull, event_str_parse
from mastodon import Mastodon, MastodonServerError

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

# Post indefinitely every 30 mins
while True:
    try:
        event_text, event_pics_d = list_pull.pull_event('./lists/event_list.json')
        parsed_text, pics = event_str_parse.parse_event(event_text=event_text, event_pics_d=event_pics_d)

        bot.twt_post(twt_api=twt_api, twt_client=twt_client, parsed_text=parsed_text, pics=pics)
        bot.mstdn_post(mstdn_client=mstdn_client, parsed_text=parsed_text, pics=pics)

        sleep(30 * 60)
    except TweepyException as e:
        logging.log_error_twt(f'main.py: {e}')
        sleep(30 * 60)
    except MastodonServerError as e:
        logging.log_error_mstdn(f'main.py: {e}')
        sleep(30 * 60)
