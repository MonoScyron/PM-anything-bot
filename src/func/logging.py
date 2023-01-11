"""
Custom logging in run.log file
"""

from datetime import datetime


def log_response(response):
    """
    Logs a tweet response in run.log
    :param response:Response to be logged
    :return: None
    """
    with open("./run.log", 'a') as log:
        w = str(datetime.now()) + " - " + str(response) + "\n"
        log.write(w)
        log.close()


def log_error(error):
    """
    Logs an error in run.log
    :param error:Error to be logged
    :return: None
    """
    with open("./run.log", 'a') as log:
        w = str(datetime.now()) + " - ERROR - " + str(error) + "\n"
        log.write(w)
        log.close()


def log_info(info):
    """
    Logs information in run.log
    :param info:Message to be logged
    :return: None
    """
    with open("./run.log", 'a') as log:
        w = str(datetime.now()) + " - Info - " + str(info) + "\n"
        log.write(w)
        log.close()
