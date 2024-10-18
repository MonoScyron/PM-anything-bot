"""
Custom logging in run.log file
"""
import sys
from datetime import datetime

logpath = "run.log"


def log_error(error):
    """
    Logs a general error in run.log
    :param error:Error to be logged
    :return: None
    """
    with open(logpath, 'a') as log:
        w = str(datetime.now()) + " - ERROR - " + str(error) + "\n"
        sys.stderr.write(w)
        log.write(w)
        log.close()


def log_error_bsky(error):
    """
    Logs a Bluesky error in run.log
    :param error:Error to be logged
    :return: None
    """
    with open(logpath, 'a') as log:
        w = str(datetime.now()) + " - ERROR Bluesky - " + str(error) + "\n"
        sys.stderr.write(w)
        log.write(w)
        log.close()


def log_error_twt(error):
    """
    Logs a Twitter error in run.log
    :param error:Error to be logged
    :return: None
    """
    with open(logpath, 'a') as log:
        w = str(datetime.now()) + " - ERROR Twitter - " + str(error) + "\n"
        sys.stderr.write(w)
        log.write(w)
        log.close()


def log_error_mstdn(error):
    """
    Logs a Mastodon error in run.log
    :param error:Error to be logged
    :return: None
    """
    with open(logpath, 'a') as log:
        w = str(datetime.now()) + " - ERROR Mastodon - " + str(error) + "\n"
        sys.stderr.write(w)
        log.write(w)
        log.close()


def log_info_bsky(info):
    """
    Logs Bluesky information in run.log
    :param info:Message to be logged
    :return: None
    """
    with open(logpath, 'a') as log:
        w = str(datetime.now()) + " - Info Bluesky - " + str(info) + "\n"
        log.write(w)
        log.close()


def log_info_twt(info):
    """
    Logs Twitter information in run.log
    :param info:Message to be logged
    :return: None
    """
    with open(logpath, 'a') as log:
        w = str(datetime.now()) + " - Info Twitter - " + str(info) + "\n"
        log.write(w)
        log.close()


def log_info_mstdn(info):
    """
    Logs Mastodon information in run.log
    :param info:Message to be logged
    :return: None
    """
    with open(logpath, 'a') as log:
        w = str(datetime.now()) + " - Info Mastodon - " + str(info) + "\n"
        log.write(w)
        log.close()
