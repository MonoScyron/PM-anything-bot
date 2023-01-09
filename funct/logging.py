from datetime import datetime


def log_action(response):
    with open("run.log", 'a') as log:
        w = str(datetime.now()) + " - " + str(response) + "\n"
        log.write(w)
        log.close()
