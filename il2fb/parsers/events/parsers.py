# coding: utf-8

from pyparsing import ParseException

from .exceptions import EventParsingError
from .grammar.events import all_rules


__all__ = (
    'EventsParser', 'SelectiveEventsParser', 'InclusiveEventsParser',
    'ExclusiveEventsParser',
)


class EventsParser(object):

    def __init__(self, rules=None):
        self._rules = rules if rules is not None else all_rules

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


class SelectiveEventsParser(EventsParser):

    def __init__(self, rules, condition):
        rules = list(filter(condition, all_rules))
        super(SelectiveEventsParser, self).__init__(rules)

    def parse_string(self, string):
        return (super(SelectiveEventsParser, self)
                .parse_string(string, ignore_errors=True))


class InclusiveEventsParser(SelectiveEventsParser):

    def __init__(self, includes):
        super(InclusiveEventsParser, self).__init__(
            includes, condition=lambda x: x.structure in includes)


class ExclusiveEventsParser(SelectiveEventsParser):

    def __init__(self, excludes):
        super(ExclusiveEventsParser, self).__init__(
            excludes, condition=lambda x: x.structure not in excludes)
