"""
Manipulation of the bot via API
"""
import atproto
import tweepy
from mastodon import Mastodon, MastodonError
from tweepy import TweepyException

import bot_logging


def bsky_post(bsky_client: atproto.Client, parsed_text, pics, log=False) -> None:
    """
    Send a random Bluesky post from the ProjectMoon Anything Bot and logs the response
    :param bsky_client: Authenticated client of the bot on Bluesky
    :param parsed_text: Text for bot to post
    :param pics: File paths to the pics for the bot to post
    :param log: Whether to log info messages
    :return: None
    """
    try:
        images = []
        for p in pics:
            images.append(open(p, mode='rb'))
        post = bsky_client.send_images(text=parsed_text, images=[img.read() for img in images])
        for img in images:
            img.close()

        if log:
            bot_logging.log_info_bsky(f'uri={post.uri}, cid={post.cid}')
    except Exception as e:
        bot_logging.log_error_bsky(f'bot.py: {e}')


def twt_post(twt_api: tweepy.API, twt_client: tweepy.Client, parsed_text, pics, log=False) -> None:
    """
    Send a random tweet from the ProjectMoon Anything Bot and logs the response
    :param twt_api: Authenticated API of the bot
    :param twt_client: Authenticated client of the bot on Twitter
    :param parsed_text: Text for bot to post
    :param pics: File paths to the pics for the bot to post
    :param log: Whether to log info messages
    :return: None
    """
    try:
        twt_media_ids = []
        for p in pics:
            twt_media_ids.append(twt_api.media_upload(filename=p).media_id_string)

        res = twt_client.create_tweet(text=parsed_text, media_ids=twt_media_ids)
        if res.errors:
            bot_logging.log_error_twt(res)
        elif log:
            bot_logging.log_info_twt(res.data)
    except TweepyException as e:
        bot_logging.log_error_twt(f'bot.py: {e}')


def mstdn_post(mstdn_client: Mastodon, parsed_text, pics, log=False) -> None:
    """
    Send a random post on Mastodon from the ProjectMoon Anything Bot and logs the response
    :param mstdn_client: Authenticated client of the bot on Mastodon
    :param parsed_text: Text for bot to post
    :param pics: File paths to the pics for the bot to post
    :param log: Whether to log info messages
    :return: None
    """
    try:
        mstdn_media_ids = []
        for p in pics:
            mstdn_media_ids.append(mstdn_client.media_post(media_file=p).id)

        res = mstdn_client.status_post(status=parsed_text, media_ids=mstdn_media_ids)

        modified_media_attachments = []
        for m in res.media_attachments:
            modified_media_attachments.append(m.url)
        res_dict = {
            'url': res.url,
            'content': res.content,
            'media_attachments': modified_media_attachments
        }

        if log:
            bot_logging.log_info_mstdn(f'{res_dict}')
    except MastodonError as e:
        bot_logging.log_error_mstdn(f'bot.py: {e}')
