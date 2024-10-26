import json
import os.path
import unittest
import tracery

from eventparser import EventParser, get_bot_tracery_generator


class Verify(unittest.TestCase):
    def setUp(self):
        file_path = 'tracery.json'
        self.parser = EventParser(log_error=False)
        json_file = open(file_path)
        self.trace_obj: dict = json.load(json_file)
        json_file.close()

    def test_events_nDef_and_images(self):
        for k in self.trace_obj.keys():
            event_list = self.trace_obj[k]
            for event in event_list:
                self.assertNotRegex(event,
                                    r'\#\w+\.\w+\.nDef\#',
                                    f'{event} has invalid use of nDef: nDef should always be at start of modifier chain')
                if k != 'event':
                    self.assertFalse(event.startswith('{'),
                                     f'{event}: Images should be put at end of expression (unless top lvl #event#)')

                raw_text = self.parser.flatten(event)
                text, pics = self.parser.parse_raw_text(raw_text)

                for pic in pics:
                    self.assertTrue(os.path.exists(pic), msg=f'No such path exists from {os.getcwd()}: {pic}')
                    self.assertLessEqual(os.path.getsize(pic), 950000, msg=f'Picture is too large {os.getcwd()}: {pic}')

    def test_parse_pics(self):
        text, pics = self.parser.parse_raw_text('{testImg1}text1{testImg2}text2{testImg3}')
        self.assertEqual(text, 'text1text2')
        self.assertEqual(pics, ['testImg1', 'testImg2', 'testImg3'])

    def test_modifier_possessive(self):
        grammar = {
            'origin': '#test.possessive#',
            'test': 'tests'
        }

        gen = get_bot_tracery_generator(grammar)
        s = gen.flatten('#origin#')
        self.assertEqual(s, "tests's")

    def test_modifier_nDef(self):
        grammar = {
            'origin': '#test1.nDef##test2.nDef##test3.nDef##test4.nDef##test5.nDef#',
            'test1': 'test1',
            'test2': 'thetest2',
            'test3': 'the     test3',
            'test4': 'The test4',
            'test5': ' test5'
        }

        gen = get_bot_tracery_generator(grammar)
        s = gen.flatten('#origin#')
        self.assertEqual(s, "test1test2test3test4 test5")

    def test_modifier_frontHalf(self):
        grammar = {
            'origin': '#test1.frontHalf##test2.frontHalf##test3.frontHalf##test4.frontHalf#',
            'test1': 'a',
            'test2': 'b_{img1}',
            'test3': 'c__',
            'test4': '{img2}'
        }

        gen = get_bot_tracery_generator(grammar)
        s = gen.flatten('#origin#')
        self.assertEqual(s, "b{img1}c{img2}")

    def test_modifier_backHalf(self):
        grammar = {
            'origin': '#test1.backHalf##test2.backHalf##test3.backHalf##test4.backHalf#',
            'test1': 'a',
            'test2': '_b',
            'test3': '_cc',
            'test4': ''
        }

        gen = get_bot_tracery_generator(grammar)
        s = gen.flatten('#origin#')
        self.assertEqual(s, "abcc")

    def test_modifier_s(self):
        grammar = {
            'origin': '#test.s#',
            'test': 'test{img}'
        }

        gen = get_bot_tracery_generator(grammar)
        s = gen.flatten('#origin#')
        self.assertEqual(s, "tests{img}")


if __name__ == '__main__':
    unittest.main()
