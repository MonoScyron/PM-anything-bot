import json
import re
import sys

from eventparser import EventParser

file_path = 'tracery.json'
parser = EventParser(file_path=file_path, log=False)
json_file = open(file_path)
trace_obj: dict = json.load(json_file)
json_file.close()

for k in trace_obj.keys():
    event_list = trace_obj[k]
    for event in event_list:
        if re.search(r'\#\w+\.\w+\.nDef\#', event):
            sys.stdout.write(f'\033[91m"{event}" has invalid use of nDef\033[0m')
            exit(1)

        raw_text = parser.flatten(event)
        text, pics = parser.parse_raw_text(raw_text)

        for pic in pics:
            p = open(pic)
            p.close()

        print(f'{event}')
