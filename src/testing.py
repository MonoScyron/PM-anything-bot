import json

from func import event_str_parse, list_pull


def check_images():
    """
    Checks through pull and event lists and makes sure all images are valid
    :return:None
    """
    pull_file = open('lists/pull_list.json')
    pull_list = json.load(pull_file)
    pull_file.close()

    for k in pull_list.keys():
        curr_d = pull_list[k]
        for curr_k in curr_d.keys():
            open(f'{curr_d[curr_k]}')

    event_file = open('lists/event_list.json')
    event_list = json.load(event_file)
    event_file.close()

    event_list = event_list['events']

    for curr_d in event_list:
        if 'event_pic' in curr_d:
            for k in curr_d['event_pic']:
                open(f'{curr_d["event_pic"][k]}')


def test_list_pull():
    """
    Pulls events from test_list.json
    :return:None
    """
    event_text, event_pics_d = list_pull.pull_event(pull_path='./lists/test_event_list.json')
    parsed_text, pics = event_str_parse.parse_event(event_text=event_text, event_pics_d=event_pics_d,
                                                    char_path='./lists/test_pull_list.json')
    print(f'{parsed_text} - {pics}')


check_images()
test_list_pull()
