import json
import re
from typing import Tuple

import tracery
from tracery.modifiers import base_english

import bot_logging


class TraceryModifierError(Exception):
    """
    Raised when a tracery modifier isn't found
    """

    def __init__(self, err_text, msg="Tracery modifier not found!"):
        self.text = err_text
        self.message = msg
        super().__init__(self.message)


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

        raw_text = self.__parser.flatten("#event#")

        if '((' in raw_text:
            bot_logging.log_error(f'eventparser.py: TraceryModifierError in "{raw_text}"')
            raise TraceryModifierError(raw_text)

        split_text = re.split("({.*?})", raw_text)

        pics = []
        for i, t in enumerate(split_text):
            if '{' in t and '}' in t:
                split_text.pop(i)
                t = t.removeprefix('{').removesuffix('}')
                pics.append(t)

        text = ' '.join([t for t in split_text])

        return text, pics


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
