"""
Manipulate raw event objects from event lists
"""

from typing import Tuple
from src.func import list_pull, logging


def parse_event(event_text, event_pics_d) -> Tuple[str, list[str]]:
    """
    Parses an event from the event list
    :param event_text:Unparsed text of the event
    :param event_pics_d:Event pictures dictionary
    :return:Parsed text of the event, list of pictures to upload in order
    """
    parsed_text, pics = parse_event_text(text=event_text)

    if event_pics_d:
        keys = event_pics_d.keys()
        for k in keys:
            pics.insert(int(k), event_pics_d[k])

    return parsed_text, pics


def parse_event_text(text) -> Tuple[str, list[str]]:
    """
    Parses event texts, pulling characters as needed
    :param text:Unparsed text of the event
    :return:Parsed text of the event, list of pictures to upload in order
    """
    split_text = text.split('$')
    split_text = [x for x in split_text if len(x) > 0]

    pics = []

    for i in range(len(split_text)):
        t = split_text[i]
        if t[0] == '{':
            case = t.split('}')[0][1:]
            t = t.split('}')[1]
            if case == "CHAR":
                name, pic = list_pull.pull_character(True)
                split_text[i] = name + t
                pics.append(pic)
            elif case == "char":
                name, pic = list_pull.pull_character(False)
                split_text[i] = name + t
                pics.append(pic)
            elif case == "FACTION":
                name, pic = list_pull.pull_faction(True)
                split_text[i] = name + t
                pics.append(pic)
            elif case == "faction":
                name, pic = list_pull.pull_faction(False)
                split_text[i] = name + t
                pics.append(pic)
            else:
                logging.log_error("event_str_parse.py couldn't find case for parsing event text.")

    parsed_text = ""
    for t in split_text:
        parsed_text += t

    return parsed_text, pics
