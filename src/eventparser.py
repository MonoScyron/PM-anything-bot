import json
from typing import Tuple

import tracery
from tracery.modifiers import base_english


# TODO: Rework for tracery

class EventParser:
    """
    Manipulate raw event string from tracery json
    """

    def __init__(self, file_path='tracery.json'):
        json_file = open(file_path)
        parser = tracery.Grammar(json.load(json_file))
        json_file.close()

        parser.add_modifiers(base_english)
        parser.add_modifiers(added_mods)
        self.__parser = parser

    def parse_event(self) -> Tuple[str, list[str]]:
        """
        Parses an event from the event list
        :param file_path: Path of the tracery file
        :return:Parsed text of the event, list of pictures to upload in order
        """

        return self.__parser.flatten("#event#")

        # return text, pics


def possessive(text: str, *params):
    return text + "'s"


def nDef(text: str, *params):
    if text[0:3].lower() == 'the':
        return text[3:].strip()
    else:
        return text


added_mods = {
    'possessive': possessive,
    'nDef': nDef
}
