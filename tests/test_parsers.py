# -*- coding: utf-8 -*-

from profilehooks import timecall

from il2fb.parsers.events import parse_string
from il2fb.parsers.events.exceptions import EventParsingError
from il2fb.parsers.events.structures import events

from .base import BaseTestCase


class ParsersTestCase(BaseTestCase):

    def setUp(self):
        self.structures = (getattr(events, name) for name in events.__all__)

    @staticmethod
    def get_event_examples(structure):
        doc = structure.__doc__.strip().replace('::', ':').replace('    ', '')
        return (
            x[1:-1] for x in doc.splitlines()
            if x.startswith('"') and x.endswith('"')
        )

    def test_parse_string(self):
        profiled_parse_string = timecall(immediate=False)(parse_string)

        for structure in self.structures:
            for example in self.get_event_examples(structure):
                event = profiled_parse_string(example)
                self.assertIsInstance(event, structure)

    def test_parse_string_with_unexpected_data(self):
        string = "foo bar baz quz"
        try:
            parse_string(string)
        except EventParsingError:
            pass
        else:
            self.fail("Parsing \"{0}\" was expected to raise EventParsingError"
                      .format(string))
