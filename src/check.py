import json
import eventparser


# TODO: Rework for tracery

def check_all():
    """
    Checks through pull and event lists and makes sure all images/queries are valid
    :return:None
    """
    pull_file = open('lists/tracery.json')
    pull_list = json.load(pull_file)
    pull_file.close()

    for k in pull_list.keys():
        curr_d = pull_list[k]
        for curr_k in curr_d.keys():
            open(f'{curr_d[curr_k]}')

    event_file = open('tracery.json')
    event_list = json.load(event_file)
    event_file.close()

    event_list = event_list['events']

    for curr_d in event_list:
        if 'event_text' not in curr_d:
            sub_event_list = curr_d['sub_events']
            for sub_curr_d in sub_event_list:
                sub_event_text, _ = event_str_parse.parse_event_text(sub_curr_d['event_text'], 'lists/tracery.json')
                print(sub_event_text)
                if 'event_pic' in sub_curr_d:
                    for k in sub_curr_d['event_pic']:
                        open(f'{sub_curr_d["event_pic"][k]}')
        else:
            event_text, _ = event_str_parse.parse_event_text(curr_d['event_text'], 'lists/tracery.json')
            print(event_text)
            if 'event_pic' in curr_d:
                for k in curr_d['event_pic']:
                    open(f'{curr_d["event_pic"][k]}')


# bot_api, bot_client = get_api_client()
check_all()
