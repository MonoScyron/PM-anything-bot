"""
Pull objects from list files
"""

import json
import random
from typing import Tuple, Union
from func import logging


# noinspection PyBroadException
def pull_event(pull_path) -> Tuple[str, Union[dict, None]]:
    """
    Pulls a random event from the list of events
    :param pull_path: Path of the event pull file
    :return: Unparsed tweet text, event pictures dictionary if applicable
    """
    pull_file = open(pull_path)
    pull_list = json.load(pull_file)

    events = pull_list['events']
    c_index = random.randrange(0, len(events))
    event = events[c_index]

    pull_file.close()

    try:
        if 'event_text' not in event:
            events = event['sub_events']
            c_index = random.randrange(0, len(events))
            event = events[c_index]

        event_text = event['event_text']
        if 'event_pic' in event:
            event_pics_d = event['event_pic']
            return event_text, event_pics_d
        else:
            return event_text, None

    except Exception:
        error_msg = f'pull_event(): {event}'
        logging.log_error(error_msg)


def pull_character(is_cap, pull_path, is_def=True, is_plural=False) -> Tuple[str, str]:
    """
    Pulls a random character from the list of characters
    :param is_cap:Whether to capitalize "the" in a character's title
    :param pull_path: Path of the character pull file
    :param is_def:Whether to include the definitive of a character ("The")
    :param is_plural:Whether character name should be plural
    :return:Character name, path to character's picture
    """
    pull_file = open(pull_path)
    pull_list = json.load(pull_file)
    chars_d = pull_list['chars']
    abnos_d = pull_list['abnos']
    pull_file.close()

    chars_d = chars_d | abnos_d
    char, char_pic_path = random.choice(list(chars_d.items()))

    if char[:3] == "The":
        if not is_def:
            char = char[4:]
        elif not is_cap:
            char = "the" + char[3:]

    if is_plural:
        if char[-1] == 's':
            char += "'s"
        else:
            char += 's'

    return char, char_pic_path


def pull_faction(is_cap, pull_path) -> Tuple[str, str]:
    """
    Pulls a random faction from the list of factions
    :param is_cap:Whether to capitalize "the" in a faction's title
    :param pull_path: Path of the faction pull file
    :return:Faction name, path to faction's icon
    """
    pull_file = open(pull_path)
    pull_list = json.load(pull_file)
    factions_d = pull_list['factions']
    pull_file.close()

    faction, faction_pic_path = random.choice(list(factions_d.items()))

    if not is_cap and faction[:3] == "The":
        faction = "the" + faction[3:]

    return faction, faction_pic_path


def pull_song(is_cap, pull_path) -> Tuple[str, str]:
    """
    Pulls a random song from the list of songs
    :param is_cap:Whether to capitalize "the" in a song's title
    :param pull_path: Path of the faction pull file
    :return:Song name, path to faction's icon
    """
    pull_file = open(pull_path)
    pull_list = json.load(pull_file)
    songs_d = pull_list['songs']
    pull_file.close()

    song, song_pic_path = random.choice(list(songs_d.items()))

    if not is_cap and song[:3] == "The":
        song = "the" + song[3:]

    return song, song_pic_path
