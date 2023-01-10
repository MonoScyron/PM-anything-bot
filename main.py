import tweepy
from time import sleep
from dotenv import dotenv_values
from func import logging, event_str_parse, list_pull

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
    event_text, event_pics_d = list_pull.pull_event()
    parsed_text, pics = event_str_parse.parse_event(event_text=event_text, event_pics_d=event_pics_d)

    media_ids = []
    for p in pics:
        media_ids.append(api.media_upload(filename=p).media_id_string)
    res = client.create_tweet(text=parsed_text, media_ids=media_ids)

    logging.log_action(res)
    sleep(30 * 60)
