import json
from func import logging


def check_images():
    """
    Checks through pull file and makes sure all images are valid
    :return:None
    """
    pull_file = open('../lists/pull_list.json')
    pull_list = json.load(pull_file)
    pull_file.close()

    for k in pull_list.keys():
        curr_d = pull_list[k]
        for curr_k in curr_d.keys():
            open(f'.{curr_d[curr_k]}')


def check_logs():
    """
    Checks to see if run.log is in the correct position
    :return:None
    """
    logging.log_info("This is a test!")


check_logs()
check_images()
