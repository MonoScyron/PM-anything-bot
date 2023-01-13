"""
Manipulate raw event objects from event lists
"""

from typing import Tuple
from func import list_pull, logging


def parse_event(event_text, event_pics_d, char_path='./lists/pull_list.json') -> \
        Tuple[str, list[str]]:
    """
    Parses an event from the event list
    :param event_text:Unparsed text of the event
    :param event_pics_d:Event pictures dictionary
    :param char_path: Path of the character pull file
    :return:Parsed text of the event, list of pictures to upload in order
    """
    parsed_text, pics = parse_event_text(text=event_text, char_path=char_path)

    if event_pics_d:
        keys = event_pics_d.keys()
        for k in keys:
            pics.insert(int(k), event_pics_d[k])

    return parsed_text, pics


def parse_event_text(text, char_path) -> Tuple[str, list[str]]:
    """
    Parses event texts, pulling characters as needed
    :param text:Unparsed text of the event
    :param char_path: Path of the character pull file
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

            name, pic = None, None
            # Pull necessary chars/factions with list_pull
            if case == "CHAR":
                name, pic = list_pull.pull_character(True, pull_path=char_path)
            elif case == "char":
                name, pic = list_pull.pull_character(False, pull_path=char_path)
            elif case == "char-D":
                name, pic = list_pull.pull_character(False, pull_path=char_path, is_def=False)
            elif case == "FACTION":
                name, pic = list_pull.pull_faction(True, pull_path=char_path)
            elif case == "faction":
                name, pic = list_pull.pull_faction(False, pull_path=char_path)
            else:
                logging.log_error("event_str_parse.py couldn't find case for parsing event text.")

            split_text[i] = name + t
            pics.append(pic)

    parsed_text = ""
    for t in split_text:
        parsed_text += t

    return parsed_text, pics
