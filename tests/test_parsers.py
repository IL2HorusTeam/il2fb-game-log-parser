# coding: utf-8

from il2fb.parsers.events import (
    EventsParser, InclusiveEventsParser, ExclusiveEventsParser,
)
from il2fb.parsers.events.exceptions import EventParsingError
from il2fb.parsers.events.structures import events

from .base import BaseTestCase


class EventsParserBaseTestCase(BaseTestCase):

    def setUp(self):
        self.structures = (getattr(events, name) for name in events.__all__)

    @staticmethod
    def get_event_examples(structure):
        doc = structure.__doc__.strip().replace('::', ':').replace('    ', '')
        return (
            x[1:-1] for x in doc.splitlines()
            if x.startswith('"') and x.endswith('"')
        )


class EventsParserTestCase(EventsParserBaseTestCase):

    def setUp(self):
        super(EventsParserTestCase, self).setUp()
        self.parser = EventsParser()

    def test_parse_string(self):
        for structure in self.structures:
            for example in self.get_event_examples(structure):
                event = self.parser.parse_string(example)
                self.assertIsInstance(event, structure)

    def test_parse_string_with_unexpected_data(self):
        string = "foo bar baz quz"
        try:
            self.parser.parse_string(string)
        except EventParsingError:
            pass
        else:
            self.fail("Parsing \"{0}\" was expected to raise EventParsingError"
                      .format(string))

    def test_parse_string_with_invalid_data(self):
        string = "[99:99:99 PM] Mission BEGIN"
        try:
            self.parser.parse_string(string)
        except ValueError:
            pass
        else:
            self.fail("Parsing \"{0}\" was expected to raise ValueError"
                      .format(string))

    def test_parse_string_safely(self):
        self.assertIsNone(self.parser.parse_string("foo bar baz quz", ignore_errors=True))
        self.assertIsNone(self.parser.parse_string("[99:99:99 PM] Mission BEGIN", ignore_errors=True))


class InclusiveEventsParserTestCase(EventsParserBaseTestCase):

    def test_inclusive_events_parser(self):
        includes = [events.HumanHasConnected, events.HumanHasSelectedAirfield]
        parser = InclusiveEventsParser(includes)

        for structure in self.structures:
            for example in self.get_event_examples(structure):
                event = parser.parse_string(example)
                if structure in includes:
                    self.assertIsInstance(event, structure)
                else:
                    self.assertIsNone(event)

        self.assertIsNone(parser.parse_string("foo bar baz quz"))
        self.assertIsNone(parser.parse_string("[99:99:99 PM] Mission BEGIN"))


class ExclusiveEventsParserTestCase(EventsParserBaseTestCase):

    def test_exclusive_events_parser(self):
        excludes = [
            events.TreeWasDestroyed, events.TreeWasDestroyedByAIAircraft,
            events.TreeWasDestroyedByStatic,
            events.TreeWasDestroyedByHumanAircraft,
        ]
        parser = ExclusiveEventsParser(excludes)

        for structure in self.structures:
            for example in self.get_event_examples(structure):
                event = parser.parse_string(example)
                if structure in excludes:
                    self.assertIsNone(event)
                else:
                    self.assertIsInstance(event, structure)

        self.assertIsNone(parser.parse_string("foo bar baz quz"))
        self.assertIsNone(parser.parse_string("[99:99:99 PM] Mission BEGIN"))
