"""
Pull objects from list files
"""

import json
import random
from typing import Tuple, Union


def pull_event() -> Tuple[str, Union[dict, None]]:
    """
    Pulls a random event from the list of events
    :return: Unparsed tweet text, event pictures dictionary if applicable
    """
    pull_file = open('./lists/event_list.json')
    pull_list = json.load(pull_file)
    events = pull_list['events']
    pull_file.close()

    c_index = random.randrange(0, len(events))
    event = events[c_index]
    event_text = event['event_text']
    if 'event_pic' in event:
        event_pics_d = event['event_pic']
        return event_text, event_pics_d
    else:
        return event_text, None


def pull_character(is_cap) -> Tuple[str, str]:
    """
    Pulls a random character from the list of characters
    :param is_cap:Whether to capitalize "the" in a character's title
    :return:Character name, path to character's picture
    """
    pull_file = open('./lists/pull_list.json')
    pull_list = json.load(pull_file)
    chars_d = pull_list['chars']
    abnos_d = pull_list['abnos']
    pull_file.close()

    chars_d = chars_d | abnos_d
    char, char_pic_path = random.choice(list(chars_d.items()))

    if not is_cap and char[:3] == "The":
        char = "the" + char[3:]

    return char, char_pic_path


def pull_faction(is_cap) -> Tuple[str, str]:
    """
    Pulls a random faction from the list of factions
    :param is_cap:Whether to capitalize "the" in a faction's title
    :return:Faction name, path to faction's icon
    """
    pull_file = open('./lists/pull_list.json')
    pull_list = json.load(pull_file)
    factions_d = pull_list['factions']
    pull_file.close()

    faction, faction_pic_path = random.choice(list(factions_d.items()))

    if not is_cap and faction[:3] == "The":
        faction = "the" + faction[3:]

    return faction, faction_pic_path
