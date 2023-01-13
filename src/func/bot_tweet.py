"""
Manipulation of the Twitter bot via API
"""

from func import event_str_parse, list_pull, logging


def bot_tweet(bot_api, bot_client):
    """
    Send a random tweet from the Project Moon Anything Bot and logs the response
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
    else:
        logging.log_response(res)
