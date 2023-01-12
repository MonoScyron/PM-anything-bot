import json


def check_images():
    """
    Checks through pull and event lists and makes sure all images are valid
    :return:None
    """
    pull_file = open('../lists/pull_list.json')
    pull_list = json.load(pull_file)
    pull_file.close()

    for k in pull_list.keys():
        curr_d = pull_list[k]
        for curr_k in curr_d.keys():
            open(f'.{curr_d[curr_k]}')

    event_file = open('../lists/event_list.json')
    event_list = json.load(event_file)
    event_file.close()

    event_list = event_list['events']

    for curr_d in event_list:
        if 'event_pic' in curr_d:
            for k in curr_d['event_pic']:
                open(f'.{curr_d["event_pic"][k]}')


check_images()
