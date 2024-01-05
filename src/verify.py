import json
import os.path
import re
import sys

from eventparser import EventParser

file_path = 'tracery.json'
parser = EventParser(file_path=file_path, log_error=False)
json_file = open(file_path)
trace_obj: dict = json.load(json_file)
json_file.close()

for k in trace_obj.keys():
    event_list = trace_obj[k]
    for event in event_list:
        if re.search(r'\#\w+\.\w+\.nDef\#', event):
            sys.stderr.write(f'"{event}" has invalid use of nDef')
            exit(1)

        raw_text = parser.flatten(event)
        text, pics = parser.parse_raw_text(raw_text)

        for pic in pics:
            if not os.path.exists(pic):
                sys.stderr.write(f'No such path exists from {os.getcwd()}: {pic}')
                exit(1)

        print(f'{event}')
