import tweepy
from dotenv import dotenv_values

from funct import logging

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

# Tweet
media = api.media_upload(filename="./img/test.jpg")
res = client.create_tweet(text="Punishment Bird tweets", media_ids=[media.media_id_string])
logging.log_action(res)

# TODO: Download characters images from LobCorp
# TODO: Download characters images from Library of Ruina
# TODO: Set up random anything tweet generator
# TODO: Set up Google Cloud server to run bot
