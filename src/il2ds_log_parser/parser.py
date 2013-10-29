# -*- coding: utf-8 -*-

import datetime
import re

from il2ds_log_parser.constants import LOG_TIME_FORMAT, LOG_DATE_FORMAT
from il2ds_log_parser.events import *
from il2ds_log_parser.regex import *


__all__ =  [
    'TimeStampedRegexParser', 'DateTimeStampedRegexParser',
    'NumeratedRegexParser', 'FuelRegexParser', 'PositionedRegexParser',
    'SeatRegexParser', 'VictimOfUserRegexParser', 'VictimOfStaticRegexParser',
    'SeatVictimOfUserRegexParser', 'MultipleParser', 'RegistrationError',
    'default_evt_parser',
]


def parse_time(value):
    """Take time in '%I:%M:%S %p' format and convert it to ISO format."""
    dt = datetime.datetime.strptime(value, LOG_TIME_FORMAT)
    return dt.time()


def parse_date(value):
    """Take date in '%b %d, %Y' format and convert it to ISO format."""
    dt = datetime.datetime.strptime(value, LOG_DATE_FORMAT)
    return dt.date()


class TimeStampedRegexParser(object):

    """Parse a line which has a time stamp at the beginning."""

    def __init__(self, regex, evt_type=None):
        """
        Input:
        `regex`             # verbose regular expression which contains
                            # 'time' group;

        `evt_type`          # type which will be added to a matched event.
                            # Default value: `None`.
        """
        self.rx = re.compile(regex, RX_FLAGS)
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
            TimeStampedRegexParser.update_time(evt)
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

    @staticmethod
    def update_time(evt):
        """
        Convert event's time to ISO format.

        Input:
        `evt`               # A dictionary with 'time' key which stores event's
                            # time in '%I:%M:%S %p' format.

        Transformation:
        Convert 'time' value of input dictionary to ISO format.
        """
        evt['time'] = parse_time(evt.get('time'))


class DateTimeStampedRegexParser(TimeStampedRegexParser):

    """Parse a line which has a datetime stamp at the beginning."""

    def __call__(self, value):
        """
        Take a line, parse it with internal regex and return an event
        dictionary. Regex must contain 'date' and 'time' groups. Those groups
        must contain event's date and time in '%b %d, %Y' and '%I:%M:%S %p'
        formats respectively. If parser has own type, it will be added to the
        event.

        Input:
        `value`             # A string which begins with event's datetime
                            # in '[%b %d, %Y %I:%M:%S %p]' format

        Output:
        {                   # A dictionary which contains:
            'date': "DATE", # event's date value in '%Y:%m:%d' format;
            'time': "TIME", # event's time value in '%H:%M:%S' format;
            'type': "TYPE", # an optional type value specified by parser.
        }                   #
                            # Output can contain another extra values provided
                            # by groups of regex.
        """
        evt = super(DateTimeStampedRegexParser, self).__call__(value)
        if evt:
            DateTimeStampedRegexParser.update_date(evt)
        return evt

    @staticmethod
    def update_date(evt):
        """
        Convert event's date to ISO format.

        Input:
        `evt`               # A dictionary with 'date' key which stores event's
                            # date in '%b %d, %Y' format.

        Transformation:
        Convert 'date' value of input dictionary to ISO format.
        """
        evt['date'] = parse_date(evt['date'])


class NumeratedRegexParser(TimeStampedRegexParser):

    """
    Parse a line which has a time stamp at the beginning and an integer number
    in the middle.
    """

    def __call__(self, value):
        """
        Take a line, parse it with internal regex and return an event
        dictionary. Regex must contain 'time' and 'number' groups. Those groups
        must contain event's time in '%I:%M:%S %p' format and an integer number
        represented by string. If parser has own type, it will be added to the
        event.

        Input:
        `value`             # A string which begins with event's time in
                            # '[%I:%M:%S %p]' format and has an integer
                            # number in the middle.

        Output:
        {                   # A dictionary which contains:
            'time': "TIME", # event's time value in '%H:%M:%S' format;

            'number': NUMBER,   # integer number;

            'type': "TYPE", # an optional type value specified by parser.
        }                   #
                            # Output can contain another extra values provided
                            # by groups of regex.
        """
        evt = super(NumeratedRegexParser, self).__call__(value)
        if evt:
            NumeratedRegexParser.update_number(evt)
        return evt

    @staticmethod
    def update_number(evt):
        """
        Convert event's number's type from string to int.

        Input:
        `evt`               # A dictionary with 'number' key which stores
                            # an integer represented by string.

        Transformation:
        Convert 'number' value of input dictionary from string to integer.
        """
        evt['number'] = int(evt['number'])


class FuelRegexParser(TimeStampedRegexParser):

    """
    Parse a line which has a time stamp at the beginning and fuel percentage
    integer value at the end.
    """

    def __call__(self, value):
        """
        Take a line, parse it with internal regex and return an event
        dictionary. Regex must contain 'time' and 'fuel' groups. Those groups
        must contain event's time in '%I:%M:%S %p' format and fuel percentage
        integer number represented by string. If parser has own type, it will
        be added to the event.

        Input:
        `value`             # A string which begins with event's time in
                            # '[%I:%M:%S %p]' format and ends with fuel
                            # percentage integer number.

        Output:
        {                   # A dictionary which contains:
            'time': "TIME", # event's time value in '%H:%M:%S' format;
            'fuel': FUEL,   # fuel integer value;
            'type': "TYPE", # an optional type value specified by parser.
        }                   #
                            # Output can contain another extra values provided
                            # by groups of regex.
        """
        evt = super(FuelRegexParser, self).__call__(value)
        if evt:
            FuelRegexParser.update_fuel(evt)
        return evt

    @staticmethod
    def update_fuel(evt):
        """
        Convert event's fuel's type from string to int.

        Input:
        `evt`               # A dictionary with 'fuel' key which stores
                            # an integer represented by string.

        Transformation:
        Convert 'fuel' value of input dictionary from string to integer.
        """
        evt['fuel'] = int(evt['fuel'])


class PositionedRegexParser(TimeStampedRegexParser):

    """
    Parse a line which has a time stamp at the beginning and two-dimensional
    float coordinates at the end.
    """

    def __call__(self, value):
        """
        Take a line, parse it with internal regex and return an event
        dictionary. Regex must contain 'time', 'pos_x' and 'pos_y' groups.
        Those groups must contain event's time in '%I:%M:%S %p' format, x and y
        position float values represented by strings. If parser has own type,
        it will be added to the event.

        Input:
        `value`             # A string which begins with event's time in
                            # '[%I:%M:%S %p]' format and ends with
                            # two-dimensional float coordinates.

        Output:
        {                   # A dictionary which contains:
            'time': "TIME", # event's time value in '%H:%M:%S' format;
            'pos': {        # a dictionary with
                'x': X,     # float x position value;
                'y': Y,     # float y position value;
            },              #
            'type': "TYPE", # an optional type value specified by parser.
        }                   #
                            # Output can contain another extra values provided
                            # by groups of regex.
        """
        evt = super(PositionedRegexParser, self).__call__(value)
        if evt:
            PositionedRegexParser.update_pos(evt)
        return evt

    @staticmethod
    def update_pos(evt):
        """
        Wrap event's x and y string position values to a dictionary with
        float x and y position values.

        Input:
        `evt`               # A dictionary with 'pos_x' and 'pos_y' keys
                            # containing float values represented by strings.

        Transformation:
        Replace 'pos_x' and 'pos_y' string values with a single 'pos'
        dictionary containing float 'x' and 'y' values.
        """
        x = evt.pop('pos_x')
        y = evt.pop('pos_y')
        evt['pos'] = {
            'x': float(x),
            'y': float(y),
        }


class SeatRegexParser(PositionedRegexParser):

    """
    Parse a line which has a time stamp at the beginning, seat integer
    number in the middle and two-dimensional float coordinates at the end.
    """

    def __call__(self, value):
        """
        Take a line, parse it with internal regex and return an event
        dictionary. Regex must contain 'time', 'seat', 'pos_x' and 'pos_y'
        groups. Those groups must contain event's time in '%I:%M:%S %p' format,
        seat number integer value, x and y position float values represented by
        strings. If parser has own type, it will be added to the event.

        Input:
        `value`             # A string which begins with event's time in
                            # '[%I:%M:%S %p]' format, has seat integer
                            # number in the middle and and ends with
                            # two-dimensional float coordinates.

        Output:
        {                   # A dictionary which contains:
            'time': "TIME", # event's time value in '%H:%M:%S' format;
            'seat': SEAT,   # integer number of seat;
            'pos': {        # a dictionary with
                'x': X,     # float x position value;
                'y': Y,     # float y position value;
            },              #
            'type': "TYPE", # an optional type value specified by parser.
        }                   #
                            # Output can contain another extra values provided
                            # by groups of regex.
        """
        evt = super(SeatRegexParser, self).__call__(value)
        if evt:
            SeatRegexParser.update_seat(evt)
        return evt

    @staticmethod
    def update_seat(evt):
        """
        Convert event's seat number's type from string to int.

        Input:
        `evt`               # A dictionary with 'seat' key which stores an
                            # integer represented by string.

        Transformation:
        Convert 'seat' value of input dictionary from string to integer.
        """
        evt['seat'] = int(evt['seat'])


class VictimOfUserRegexParser(PositionedRegexParser):

    """
    Parse a line which has a time stamp at the beginning, enemy's callsign
    and aircraft in the middle and two-dimensional float coordinates at the
    end.
    """

    def __call__(self, value):
        """
        Take a line, parse it with internal regex and return an event
        dictionary. Regex must contain 'time', 'e_callsign', 'e_aircraft',
        'pos_x' and 'pos_y' groups. Those groups must contain event's time in
        '%I:%M:%S %p' format, enemy's callsign and aircraft string values,
        x and y position float values represented by strings. If parser has own
        type, it will be added to the event.

        Input:
        `value`             # A string which begins with event's time in
                            # '[%I:%M:%S %p]' format, has enemy's callsign and
                            # aircraft string values in the middle and and ends
                            # with two-dimensional float coordinates.

        Output:
        {                   # A dictionary which contains:
            'time': "TIME", # event's time value in '%H:%M:%S' format;
            'attacker': {   # a dictionary with attacker's

                'callsign': "CALLSIGN",     # callsign and
                'aircraft': "AIRCRAFT",     # aircraft

            },              #
            'pos': {        # a dictionary with
                'x': X,     # float x position value;
                'y': Y,     # float y position value;
            },              #
            'type': "TYPE", # an optional type value specified by parser.
        }                   #
                            # Output can contain another extra values provided
                            # by groups of regex.
        """
        evt = super(VictimOfUserRegexParser, self).__call__(value)
        if evt:
            VictimOfUserRegexParser.update_attacker(evt)
        return evt

    @staticmethod
    def update_attacker(evt):
        """
        Wrap event's enemy's callsign and aircraft string values into a
        dictionary.

        Input:
        `evt`               # A dictionary with 'e_callsign' and 'e_aircraft'
                            # keys containing attacker's callsign and aircraft
                            # values represented by strings.

        Transformation:
        Replace 'e_callsign' and 'e_aircraft' string values with a single
        'attacker' dictionary containing string 'callsign' and 'aircraft'
        values.
        """
        callsign = evt.pop('e_callsign')
        aircraft = evt.pop('e_aircraft')
        evt['attacker'] = {
            'callsign': callsign,
            'aircraft': aircraft,
        }


class VictimOfStaticRegexParser(PositionedRegexParser):

    """
    Parse a line which has a time stamp at the beginning, attacking static's
    name in the middle and two-dimensional float coordinates at the end.
    """

    def __call__(self, value):
        """
        Take a line, parse it with internal regex and return an event
        dictionary. Regex must contain 'time', 'static', 'pos_x' and 'pos_y'
        groups. Those groups must contain event's time in '%I:%M:%S %p' format,
        attacking static's name string value, x and y position float values
        represented by strings. If parser has own type, it will be added to the
        event.

        Input:
        `value`             # A string which begins with event's time in
                            # '[%I:%M:%S %p]' format, has enemy's callsign and
                            # aircraft string values in the middle and and ends
                            # with two-dimensional float coordinates.

        Output:
        {                   # A dictionary which contains:
            'time': "TIME", # event's time value in '%H:%M:%S' format;

            'attacker': "ATTACKER",     # attacking static's string name

            'pos': {        # a dictionary with
                'x': X,     # float x position value;
                'y': Y,     # float y position value;
            },              #
            'type': "TYPE", # an optional type value specified
                            # by parser.
        }                   #
                            # Output can contain another extra values provided
                            # by groups of regex.
        """
        evt = super(VictimOfStaticRegexParser, self).__call__(value)
        if evt:
            VictimOfStaticRegexParser.update_attacker(evt)
        return evt

    @staticmethod
    def update_attacker(evt):
        """
        Change attacker's dictionary key from 'static' to 'attacker'.

        Input:
        `evt`               # A dictionary with 'static' key containing
                            # attacking static's name represented by string.

        Transformation:
        Replace 'static' string value with 'attacker' string value.
        """
        attacker = evt.pop('static')
        evt['attacker'] = attacker


class SeatVictimOfUserRegexParser(PositionedRegexParser):

    """
    Parse a line which has a time stamp at the beginning, seat integer
    number, enemy's callsign and aircraft in the middle and two-dimensional
    float coordinates at the end.
    """

    def __call__(self, value):
        """
        Take a line, parse it with internal regex and return an event
        dictionary. Regex must contain 'time', 'seat', 'e_callsign',
        'e_aircraft', 'pos_x' and 'pos_y' groups. Those groups must contain
        event's time in '%I:%M:%S %p' format, seat number integer value,
        enemy's callsign and aircraft string values, x and y position float
        values represented by strings. If parser has own type, it will be added
        to the event.

        Input:
        `value`             # A string which begins with event's time in
                            # '[%I:%M:%S %p]' format, has seat integer number,
                            # enemy's callsign and aircraft string values in
                            # the middle and and ends with two-dimensional
                            # float coordinates.

        Output:
        {                   # A dictionary which contains:
            'time': "TIME", # event's time value in '%H:%M:%S' format;
            'seat': SEAT,   # integer number of seat;
            'attacker': {   # a dictionary with attacker's

                'callsign': "CALLSIGN",     # callsign and
                'aircraft': "AIRCRAFT",     # aircraft

            },              #
            'pos': {        # a dictionary with
                'x': X,     # float x position value;
                'y': Y,     # float y position value;
            },              #
            'type': "TYPE", # an optional type value specified by parser.
        }                   #
                            # Output can contain another extra values provided
                            # by groups of regex.
        """
        evt = super(SeatVictimOfUserRegexParser, self).__call__(value)
        if evt:
            SeatRegexParser.update_seat(evt)
            VictimOfUserRegexParser.update_attacker(evt)
        return evt


class RegistrationError(Exception):
    """Thrown when registering or unregistering parser goes wrong."""


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
                if isinstance(parser, TimeStampedRegexParser):
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


default_evt_parser = MultipleParser(parsers=[
    # Events of destroying
    PositionedRegexParser(RX_DESTROYED_BLD, EVT_DESTROYED_BLD),
    PositionedRegexParser(RX_DESTROYED_TREE, EVT_DESTROYED_TREE),
    PositionedRegexParser(RX_DESTROYED_STATIC, EVT_DESTROYED_STATIC),
    PositionedRegexParser(RX_DESTROYED_BRIDGE, EVT_DESTROYED_BRIDGE),

    # Events of lightning effects
    PositionedRegexParser(
        RX_TOGGLE_LANDING_LIGHTS, EVT_TOGGLE_LANDING_LIGHTS),
    PositionedRegexParser(
        RX_TOGGLE_WINGTIP_SMOKES, EVT_TOGGLE_WINGTIP_SMOKES),

    # Mission flow events
    DateTimeStampedRegexParser(RX_MISSION_PLAYING, EVT_MISSION_PLAYING),
    DateTimeStampedRegexParser(RX_MISSION_WON, EVT_MISSION_WON),
    TimeStampedRegexParser(RX_MISSION_BEGIN, EVT_MISSION_BEGIN),
    TimeStampedRegexParser(RX_MISSION_END, EVT_MISSION_END),
    NumeratedRegexParser(RX_TARGET_END, EVT_TARGET_END),

    # User state events
    TimeStampedRegexParser(RX_CONNECTED, EVT_CONNECTED),
    TimeStampedRegexParser(RX_DISCONNECTED, EVT_DISCONNECTED),
    TimeStampedRegexParser(RX_WENT_TO_MENU, EVT_WENT_TO_MENU),
    PositionedRegexParser(RX_SELECTED_ARMY, EVT_SELECTED_ARMY),

    # Aircraft events
    FuelRegexParser(RX_WEAPONS_LOADED, EVT_WEAPONS_LOADED),
    PositionedRegexParser(RX_TOOK_OFF, EVT_TOOK_OFF),
    PositionedRegexParser(RX_CRASHED, EVT_CRASHED),
    PositionedRegexParser(RX_LANDED, EVT_LANDED),

    PositionedRegexParser(RX_DAMAGED_ON_GROUND, EVT_DAMAGED_ON_GROUND),
    PositionedRegexParser(RX_DAMAGED_SELF, EVT_DAMAGED_SELF),
    VictimOfUserRegexParser(RX_DAMAGED_BY_USER, EVT_DAMAGED_BY_USER),

    PositionedRegexParser(RX_SHOT_DOWN_SELF, EVT_SHOT_DOWN_SELF),
    VictimOfUserRegexParser(
        RX_SHOT_DOWN_BY_USER, EVT_SHOT_DOWN_BY_USER),
    VictimOfStaticRegexParser(
        RX_SHOT_DOWN_BY_STATIC, EVT_SHOT_DOWN_BY_STATIC),

    # Crew member events
    SeatRegexParser(RX_SEAT_OCCUPIED, EVT_SEAT_OCCUPIED),

    SeatRegexParser(RX_KILLED, EVT_KILLED),
    SeatVictimOfUserRegexParser(RX_KILLED_BY_USER, EVT_KILLED_BY_USER),

    SeatRegexParser(RX_BAILED_OUT, EVT_BAILED_OUT),
    SeatRegexParser(RX_PARACHUTE_OPENED, EVT_PARACHUTE_OPENED),
    SeatRegexParser(RX_WOUNDED, EVT_WOUNDED),
    SeatRegexParser(RX_HEAVILY_WOUNDED, EVT_HEAVILY_WOUNDED),

    SeatRegexParser(RX_CAPTURED, EVT_CAPTURED),
])


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
        if 'time' in evt:
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
