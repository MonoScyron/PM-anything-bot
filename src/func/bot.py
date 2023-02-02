"""
Manipulation of the Twitter bot via API
"""

import tweepy
from datetime import datetime
from dotenv import dotenv_values
from tweepy import TweepyException
from time import sleep

from func import event_str_parse, list_pull, logging


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


# ! Function not fully tested nor implemented
def like_loved_tweets(client: tweepy.Client, num_get=1440, threshold=50) -> None:
    """
    Likes all "loved" tweets within a specified number of recent tweets
    :param client:Authenticated client of the bot
    :param num_get:How many recent tweets to check "loved" tweets for, cannot be greater than 3200
    :param threshold:Number of likes a tweet has to be considered "loved"
    :return:None
    """
    env = dotenv_values(".env")

    # Loop until tweets are gotten
    while True:
        try:
            tweets = tweepy.Paginator(client.get_users_tweets, env.get("BOT_ID"), exclude=['retweets', 'replies'],
                                      tweet_fields=['public_metrics'], max_results=100).flatten(limit=num_get)
            new_loved_ids = [t.id for t in tweets if
                             t.data['public_metrics']['like_count'] > threshold]
            for t_id in new_loved_ids:
                # While tweet is not liked, try to like the tweet
                flag = False
                while not flag:
                    try:
                        client.like(tweet_id=t_id)
                        flag = True
                    except TweepyException as e:
                        logging.log_error(f'like_loved_tweets() like loop - {e}')
                        sleep(1)
            return
        # If exception when trying to get last tweet, wait 10 secs then try again
        except TweepyException as e:
            logging.log_error(f'like_loved_tweets() - {e}')
            sleep(30)


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
