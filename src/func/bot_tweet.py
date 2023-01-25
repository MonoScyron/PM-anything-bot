"""
Manipulation of the Twitter bot via API
"""
import tweepy
from dotenv import dotenv_values

from func import event_str_parse, list_pull, logging

from datetime import datetime


def bot_tweet(bot_api: tweepy.API, bot_client: tweepy.Client) -> None:
    """
    Send a random tweet from the ProjectMoon Anything Bot and logs the response
    :param bot_api:Authenticated API of the bot
    :param bot_client:Authenticated client of the bot
    :return:None
    """
    event_text, event_pics_d = list_pull.pull_event('./lists/event_list.json')
    parsed_text, pics = event_str_parse.parse_event(event_text=event_text, event_pics_d=event_pics_d)

    media_ids = []
    for p in pics:
        media_ids.append(bot_api.media_upload(filename=p).media_id_string)
    res = bot_client.create_tweet(text=parsed_text, media_ids=media_ids)

    if res.errors:
        logging.log_error(res)


def get_time_since_last_tweet(bot_client: tweepy.Client) -> int:
    """
    Returns time since ProjectMoon Anything Bot's last tweet'
    :param bot_client:Authenticated client of the bot
    :return:Time since last tweet in seconds, or -1 if there was an exception
    """
    try:
        env = dotenv_values(".env")
        last_tweets = bot_client.get_users_tweets(id=bot_client.get_user(username=env.get("BOT_USERNAME")).data.id,
                                                  exclude=["retweets", "replies"],
                                                  tweet_fields="created_at",
                                                  max_results=5)
        last_tweet_time: datetime = last_tweets.data[0].created_at
        tweet_time_delta = datetime.now().timestamp() - last_tweet_time.timestamp()
        return int(tweet_time_delta)
    except tweepy.TweepyException:
        return -1
