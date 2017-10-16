# coding: utf-8

from il2fb.commons.events import EventParsingException

from .events import get_all_events
from .priority import get_event_priority


class EventsParser(object):

    def __init__(self, events=None):
        events = events if events is not None else get_all_events()
        self._events = sorted(events, key=get_event_priority)

    def parse(self, string, ignore_errors=False):
        result = None

        for event in self._events:
            result = event.from_s(string)
            if result:
                break

        if not result and not ignore_errors:
            raise EventParsingException(
                "No event was found for string \"{0}\""
                .format(string)
            )

        return result
