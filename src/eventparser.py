import json
import re
from typing import Tuple

import tracery
from tracery.modifiers import base_english

import bot_logging


class TraceryError(Exception):
    """
    Raised when tracery flattening can't find a node/modifier
    """

    def __init__(self, err_text):
        self.err_text = err_text
        super().__init__(self.err_text)


class EventParser:
    """
    Manipulate raw event string from tracery json
    """

    def __init__(self, file_path='tracery.json', log=True):
        """
        Initialize EventParser
        :param file_path: Path to tracery json file. Defaults to 'tracery.json'.
        :param log: Whether to log errors. Defaults to True.
        """

        json_file = open(file_path)
        parser = tracery.Grammar(json.load(json_file))
        json_file.close()

        parser.add_modifiers(base_english)
        parser.add_modifiers(added_mods)

        self.__parser = parser
        self.__log = log

    def parse_event(self) -> Tuple[str, list[str]]:
        """
        Parses an event from the event list
        :return: Parsed text of the event, list of pictures to upload in order
        """
        raw_text = self.flatten("#event#")
        parsed_text, pics = self.parse_raw_text(raw_text)
        return parsed_text, pics

    def flatten(self, text):
        """
        Uses tracery to flatten given text
        :param text:Text to flatten
        :return: Flattened text
        """
        raw_text = self.__parser.flatten("#event#")

        if '((' in raw_text:
            if self.__log:
                bot_logging.log_error(f'eventparser.py: TraceryError in "{raw_text}"')
            raise TraceryError(raw_text)

        return raw_text

    @staticmethod
    def parse_raw_text(raw_text) -> Tuple[str, list[str]]:
        """
        Parses raw text from tracery
        :param raw_text:Raw tracery text
        :return: Parsed text of the event, list of pictures to upload in order
        """
        split_text = re.split("({.*?})", raw_text)

        pics = []
        for i, t in enumerate(split_text):
            if '{' in t and '}' in t:
                split_text.pop(i)
                t = t.removeprefix('{').removesuffix('}')
                pics.append(t)

        return ''.join([t for t in split_text]), pics


def front_half(text: str, *params):
    if '{' in text and '}' in text:
        split = text.split('{')
        h = len(split[0]) // 2
        front = split[0][:h]
        return front + '{' + split[1]
    else:
        return text[:len(text) // 2]


def back_half(text: str, *params):
    if '{' in text and '}' in text:
        split = text.split('{')
        h = len(split[0]) // 2
        back = split[0][h:]
        return back + '{' + split[1]
    else:
        return text[len(text) // 2:]


def possessive(text: str, *params):
    return text + "'s"


def nDef(text: str, *params):
    if text[0:3].lower() == 'the':
        return text[3:].strip()
    else:
        return text


added_mods = {
    'possessive': possessive,
    'nDef': nDef,
    'frontHalf': front_half,
    'backHalf': back_half
}
