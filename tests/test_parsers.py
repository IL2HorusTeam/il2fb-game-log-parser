# coding: utf-8

import six
import unittest

from il2fb.parsers.events import EventsParser, get_all_events
from il2fb.parsers.events.exceptions import EventParsingError


class EventsParserTestCase(unittest.TestCase):

    @staticmethod
    def get_event_examples(event):
        doc = event.__doc__.strip().replace('::', ':').replace('    ', '')
        return (
            x[1:-1] for x in doc.splitlines()
            if x.startswith('"') and x.endswith('"')
        )

    def setUp(self):
        super(EventsParserTestCase, self).setUp()
        self.structures = get_all_events()
        self.parser = EventsParser(self.structures)

    def test_parse(self):
        for structure in self.structures:
            for example in self.get_event_examples(structure):
                event = self.parser.parse(example)
                self.assertIsInstance(event, structure)

    def test_parse_invalid_string(self):
        with self.assertRaises(EventParsingError) as cm:
            self.parser.parse("[99:99:99 PM] foo bar")

        self.assertEqual(
            six.text_type(cm.exception),
            "No event was found for string \"[99:99:99 PM] foo bar\""
        )

    def test_parse_invalid_string_safely(self):
        event = self.parser.parse("foo bar baz quz", ignore_errors=True)
        self.assertIsNone(event)
