# -*- coding: utf-8 -*-

from pyparsing import ParseException

from .exceptions import EventParsingError
from .grammar.events import all_rules


__all__ = (
    'parse_string', 'parse_string_safely',
    'InclusiveEventsParser', 'ExclusiveEventsParser',
)


class EventsParser(object):

    def __init__(self, rules=None):
        self._rules = rules or all_rules

    def parse_string(self, string, ignore_errors=False):
        for rule in self._rules:
            try:
                return rule.parseString(string).event
            except ParseException:
                continue
            except (SystemExit, KeyboardInterrupt):
                raise
            except:
                if ignore_errors:
                    return
                else:
                    raise

        if not ignore_errors:
            raise EventParsingError("No grammar was found for string \"{0}\""
                                    .format(string))


__parser = EventsParser()


def parse_string(string):
    return __parser.parse_string(string)


def parse_string_safely(string):
    return __parser.parse_string(string, ignore_errors=True)


class SelectiveEventsParser(EventsParser):

    def __init__(self, rules, condition):
        rules = filter(condition, all_rules)
        super(SelectiveEventsParser, self).__init__(rules)

    def parse_string(self, string):
        return (super(SelectiveEventsParser, self)
                .parse_string(string, ignore_errors=True))


class InclusiveEventsParser(SelectiveEventsParser):

    def __init__(self, includes):
        condition = lambda x: x.structure in includes
        super(InclusiveEventsParser, self).__init__(includes, condition)


class ExclusiveEventsParser(SelectiveEventsParser):

    def __init__(self, excludes):
        condition = lambda x: x.structure not in excludes
        super(ExclusiveEventsParser, self).__init__(excludes, condition)
