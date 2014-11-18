# -*- coding: utf-8 -*-

import logging
import re

from il2fb.parsers.events.content_processor import *
from il2fb.parsers.events.event_types import *
from il2fb.parsers.events.regex import *


__all__ = (
    'RegexParser', 'MultipleParser', 'RegistrationError', 'default_evt_parser',
)

LOG = logging.getLogger(__file__)


class RegexParser(object):
    """
    Parse a line which has a time stamp at the beginning.
    """

    def __init__(self, regex, processors=None, evt_type=None):
        """
        Input:
        `regex`             # verbose regular expression which contains
                            # 'time' group;

        `evt_type`          # type which will be added to a matched event.
                            # Default value: `None`.
        """
        self.rx = re.compile(regex, RX_FLAGS)
        if processors and not isinstance(processors, list):
                processors = [processors, ]
        self.processors = processors
        self.evt_type = evt_type

    def __call__(self, value):
        """
        Take a line, parse it with internal regex and return an event
        dictionary. Regex must contain 'time' group capturing event's time in
        '%I:%M:%S %p' format. If parser has own type, it will be added to the
        event.

        Input:
        `value`             # A string which begins with event's time in
                            # '[%I:%M:%S %p]' format.

        Output:
        {                   # A dictionary which contains:
            'time': "TIME", # event's time value in '%H:%M:%S' format;
            'type': "TYPE", # an optional type value specified by parser.
        }                   #
                            # Output can contain another extra values provided
                            # by groups of regex.
        """
        m = self.rx.match(value)
        if m:
            evt = m.groupdict()
            if self.evt_type:
                evt['type'] = self.evt_type
            if self.processors:
                for processor in self.processors:
                    try:
                        processor(evt)
                    except KeyError:
                        pass
                    except ValueError:
                        pass
            return evt
        return None

    def __eq__(self, other):
        """
        Compare self with another parser object. Parsers are considered to be
        equal if their regular expressions have equal patterns.

        Input:
        `other`             # A parser object to compare with.

        Output:
        `True` if object is equal to other, `False` in another case.
        """
        return self.rx.pattern == other.rx.pattern

    def __str__(self):
        """
        String representation of parser.

        Output:
        A string in `type: regex_pattern` format if parser has own type or
        internal regex pattern in the other case.
        """
        return "%s: %s" % (self.evt_type, self.rx.pattern) \
            if self.evt_type else self.rx.pattern


class RegistrationError(Exception):
    """
    Thrown when registering or unregistering parser goes wrong.
    """


class MultipleParser(object):
    """
    Combines multiple parsers with unique patterns into a chain of parsers and
    callbacks which can be called if a string will match parser's pattern.
    """

    def __init__(self, parsers=None):
        """
        Input:
        `parsers`           # Initial list of parsers or a list of tuples
                            # consisting of a parser and a callback which will
                            # be called if parsing string will match parser's
                            # pattern. Default value: `None`.
        """
        self._registered_parsers = []
        if parsers:
            for parser in parsers:
                if isinstance(parser, RegexParser):
                    parser = (parser, None)
                self._registered_parsers.append(parser)

    def _is_registered(self, (parser, callback)):
        """
        Check if a tuple consisting of parser with callback is registered in
        multiparser. A tuple is considered to be registered if registered
        parsers list has a tuple consisting of parser and callback which are
        equal to given ones. Note: a tuple's contents are compared, not the
        tuples themselves.

        Input:
        `(parser, callback)`    # A tuple containing a parser with a callback.

        Output:
        `True` if the tuple is registered, `False` in another case.
        """
        for (p, c) in self._registered_parsers:
            if p == parser and c == callback:
                return True
        return False

    def is_registered(self, parser, callback=None):
        """
        Check if a parser and a callback are registered in multiparser. They
        are considered to be registered if registered parsers list has given
        parser with callback.

        Input:
        `parser`            # A parser to check presence of;

        `callback`          # a callback to check presence of.
                            # Default value: None.

        Output:
        `True` if the parser with the callback are registered, `False` in
        another case.
        """
        return self._is_registered((parser, callback))

    def register(self, parser, callback=None):
        """
        Register parser with callback to call if a string will match parser's
        pattern. `RegistrationError` exception will be raised if they are
        already registered.

        Input:
        `parser`:           # A parser to register;

        `callback`:         # a callback to register. Default value: None.
        """
        parser_n_callback = (parser, callback)
        if self._is_registered(parser_n_callback):
            raise RegistrationError(
                "Parser is already registered: {parser}".format(parser=parser))
        self._registered_parsers.append(parser_n_callback)

    def unregister(self, parser, callback=None):
        """
        Unregister parser with callback. `RegistrationError` exception will be
        raised if they are not registered yet.

        Input:
        `parser`:           # A parser to unregister;

        `callback`:         # a callback to unregister. Default value: None.
        """
        parser_n_callback = (parser, callback)
        if not self._is_registered(parser_n_callback):
            raise RegistrationError(
                "Parser is not registered yet: {parser}".format(parser=parser))
        self._registered_parsers.remove(parser_n_callback)

    def __call__(self, value):
        """
        Take a line and parse it with registered parsers. If a string matches
        a parser's pattern, parser's callback will be called with a value
        returned by the parser. If the callback returnes a value, that value
        will be returned by this method. In other case parser's original return
        value will be returned. If the string will not match any parser,
        `None` value will be returned.

        Input:
        `value`             # A string to parse.

        Output:
        A value returned by callback if a string matched. Or a value returned
        by a registered parser if it does not have related callback or a
        callback will return no value. Or `None` if string does not match any
        parser.
        """
        for parser, callback in self._registered_parsers:
            result = parser(value)
            if result:
                if callback:
                    return callback(result) or result
                return result
        return None


def build_default_event_parser():
    time_position = [
        process_time, process_position,
    ]
    time_togle_position = [
        process_time, process_toggle_value, process_position,
    ]
    time_seat_position = [
        process_time, process_seat, process_position,
    ]
    params = (
        # Mission flow events
        (
            RX_MISSION_WON,
            [process_time, process_date, process_army, ],
            EVT_MISSION_WON
        ),
        (
            RX_MISSION_PLAYING,
            [process_time, process_date, ],
            EVT_MISSION_PLAYING
        ),
        (RX_MISSION_BEGIN, process_time, EVT_MISSION_BEGIN),
        (RX_MISSION_END, process_time, EVT_MISSION_END),
        (
            RX_TARGET_RESULT,
            [process_time, process_number, process_target_result, ],
            EVT_TARGET_RESULT
        ),
        # User state events
        (RX_CONNECTED, process_time, EVT_CONNECTED),
        (RX_DISCONNECTED, process_time, EVT_DISCONNECTED),
        (RX_WENT_TO_MENU, process_time, EVT_WENT_TO_MENU),
        (RX_SELECTED_ARMY, time_position, EVT_SELECTED_ARMY),
        # Destruction events
        (RX_DESTROYED_BLD, time_position, EVT_DESTROYED_BLD),
        (RX_DESTROYED_TREE, time_position, EVT_DESTROYED_TREE),
        (RX_DESTROYED_BRIDGE, time_position, EVT_DESTROYED_BRIDGE),
        (RX_DESTROYED_STATIC, time_position, EVT_DESTROYED_STATIC),
        # Lightning effect events
        (
            RX_TOGGLE_LANDING_LIGHTS,
            time_togle_position,
            EVT_TOGGLE_LANDING_LIGHTS
        ),
        (
            RX_TOGGLE_WINGTIP_SMOKES,
            time_togle_position,
            EVT_TOGGLE_WINGTIP_SMOKES
        ),
        # Aircraft events
        (
            RX_WEAPONS_LOADED,
            [process_time, process_fuel, process_position, ],
            EVT_WEAPONS_LOADED
        ),
        (RX_TOOK_OFF, time_position, EVT_TOOK_OFF),
        (RX_CRASHED, time_position, EVT_CRASHED),
        (RX_LANDED, time_position, EVT_LANDED),
        (RX_DAMAGED_ON_GROUND, time_position, EVT_DAMAGED_ON_GROUND),
        (RX_DAMAGED_SELF, time_position, EVT_DAMAGED_SELF),
        (
            RX_DAMAGED_BY_USER,
            [process_time, process_attacking_user, process_position, ],
            EVT_DAMAGED_BY_USER
        ),
        (RX_SHOT_DOWN_SELF, time_position, EVT_SHOT_DOWN_SELF),
        (RX_SHOT_DOWN_BY_STATIC, time_position, EVT_SHOT_DOWN_BY_STATIC),
        (
            RX_SHOT_DOWN_BY_USER,
            [process_time, process_attacking_user, process_position, ],
            EVT_SHOT_DOWN_BY_USER
        ),
        # Crew member events
        (RX_SEAT_OCCUPIED, time_seat_position, EVT_SEAT_OCCUPIED),
        (RX_KILLED, time_seat_position, EVT_KILLED),
        (
            RX_KILLED_BY_USER,
            [
                process_time, process_seat, process_attacking_user,
                process_position,
            ],
            EVT_KILLED_BY_USER
        ),
        (RX_BAILED_OUT, time_seat_position, EVT_BAILED_OUT),
        (
            RX_SUCCESSFULLY_BAILED_OUT,
            time_seat_position,
            EVT_SUCCESSFULLY_BAILED_OUT
        ),
        (RX_WOUNDED, time_seat_position, EVT_WOUNDED),
        (RX_HEAVILY_WOUNDED, time_seat_position, EVT_HEAVILY_WOUNDED),
        (RX_CAPTURED, time_seat_position, EVT_CAPTURED),
    )
    parsers = [RegexParser(*x) for x in params]
    return MultipleParser(parsers=parsers)


default_evt_parser = build_default_event_parser()


def parse_log_lines(lines, evt_parser=default_evt_parser):
    missions = []
    unparsed = []
    mission = None
    last_time = None

    def begin_mission(evt):
        return {
            'mission': evt['mission'],
            'begined': {
                'date': evt['date'],
                'time': evt['time'],
            },
            'events': {},
        }

    def end_mission(time):
        mission['ended'] = {
            'time': time,
        }
        missions.append(mission)
        return None

    for line in lines:
        if not line:
            continue
        if "3do/Tree/Line" in line:
            continue
        evt = evt_parser(line)
        if evt is None:
            unparsed.append(line)
            continue

        evt['time'] = evt['time'].isoformat()
        if 'date' in evt:
            evt['date'] = evt['date'].isoformat()

        if evt['type'] == EVT_MISSION_PLAYING:
            if mission:
                end_mission(evt['time'])
            mission = begin_mission(evt)
            last_time = None
            continue
        if evt['type'] == EVT_MISSION_END:
            mission = end_mission(evt['time'])
            continue
        if mission is None or evt['type'] == EVT_MISSION_BEGIN:
            continue
        last_time = evt['time']
        if 'callsign' in evt:
            callsign = evt.pop('callsign')
            events = mission['events'].setdefault(callsign, [])
            events.append(evt)

    if mission:
        end_mission(last_time if last_time else "N/A")

    return missions, unparsed
