# -*- coding: utf-8 -*-

import datetime
import re

from il2ds_log_parser.constants import LOG_TIME_FORMAT, LOG_DATE_FORMAT
from il2ds_log_parser.events import *
from il2ds_log_parser.regex import *


def parse_time(value):
    """Take time in format of 'H:MM:SS AM/PM' and convert it to ISO format"""
    dt = datetime.datetime.strptime(value, LOG_TIME_FORMAT)
    return dt.time().isoformat()


def parse_date(value):
    """Take date in format of 'Mon DD, YYYY' and convert it to ISO format"""
    dt = datetime.datetime.strptime(value, LOG_DATE_FORMAT)
    return dt.date().isoformat()


class TimeStampedRegexParser(object):

    def __init__(self, regex, evt_type=None):
        """Params:
           regex: verbose regular expression,
           evt_type: type which matched event will be marked with.
        """
        self.rx = re.compile(regex, RX_FLAGS)
        self.evt_type = evt_type

    def __call__(self, value):
        m = self.rx.match(value)
        if m:
            evt = m.groupdict()
            if self.evt_type:
                evt['type'] = self.evt_type
            TimeStampedRegexParser.update_time(evt)
            return evt
        return None

    def __str__(self):
        return "%s: %s" % (self.evt_type, self.rx.pattern) \
            if self.evt_type else self.rx.pattern

    @staticmethod
    def update_time(evt):
        time = evt.get('time')
        if time:
            evt['time'] = parse_time(time)


class DateTimeStampedRegexParser(TimeStampedRegexParser):

    def __call__(self, value):
        evt = super(DateTimeStampedRegexParser, self).__call__(value)
        if evt:
            DateTimeStampedRegexParser.update_date(evt)
        return evt

    @staticmethod
    def update_date(evt):
        evt['date'] = parse_date(evt['date'])


class PositionedRegexParser(TimeStampedRegexParser):

    def __call__(self, value):
        evt = super(PositionedRegexParser, self).__call__(value)
        if evt:
            PositionedRegexParser.update_pos(evt)
        return evt

    @staticmethod
    def update_pos(evt):
        x = evt.pop('pos_x')
        y = evt.pop('pos_y')
        evt['pos'] = {
            'x': float(x),
            'y': float(y),
        }


class SeatRegexParser(PositionedRegexParser):

    def __call__(self, value):
        evt = super(SeatRegexParser, self).__call__(value)
        if evt:
            SeatRegexParser.update_seat(evt)
        return evt

    @staticmethod
    def update_seat(evt):
        evt['seat'] = int(evt['seat'])


class VictimOfUserRegexParser(PositionedRegexParser):

    def __call__(self, value):
        evt = super(VictimOfUserRegexParser, self).__call__(value)
        if evt:
            VictimOfUserRegexParser.update_attacker(evt)
        return evt

    @staticmethod
    def update_attacker(evt):
        callsign = evt.pop('e_callsign')
        aircraft = evt.pop('e_aircraft')
        evt['attacker'] = {
            'callsign': callsign,
            'aircraft': aircraft,
        }


class VictimOfStaticRegexParser(PositionedRegexParser):

    def __call__(self, value):
        evt = super(VictimOfStaticRegexParser, self).__call__(value)
        if evt:
            VictimOfStaticRegexParser.update_attacker(evt)
        return evt

    @staticmethod
    def update_attacker(evt):
        attacker = evt.pop('static')
        evt['attacker'] = attacker


class SeatVictimOfUserRegexParser(PositionedRegexParser):

    def __call__(self, value):
        evt = super(SeatVictimOfUserRegexParser, self).__call__(value)
        if evt:
            SeatRegexParser.update_seat(evt)
            VictimOfUserRegexParser.update_attacker(evt)
        return evt


class RegistrationError(Exception):
    """Thrown when registering or unregistering parser goes wrong."""


class MultipleParser(object):

    def __init__(self, parsers=None):
        self._registered_parsers = []
        if parsers:
            for parser in parsers:
                if isinstance(parser, TimeStampedRegexParser):
                    parser = (parser, None)
                self._registered_parsers.append(parser)

    def _is_registered(self, (parser, callback)):
        for (p, c) in self._registered_parsers:
            if p.rx.pattern == parser.rx.pattern and c == callback:
                return True
        return False

    def is_registered(self, parser, callback=None):
        return self._is_registered((parser, callback))

    def register(self, parser, callback=None):
        parser_n_callback = (parser, callback)
        if self._is_registered(parser_n_callback):
            raise RegistrationError(
                "Parser is already registered: {parser}".format(parser=parser))
        self._registered_parsers.append(parser_n_callback)

    def unregister(self, parser, callback=None):
        parser_n_callback = (parser, callback)
        if not self._is_registered(parser_n_callback):
            raise RegistrationError(
                "Parser is not registered yet: {parser}".format(parser=parser))
        self._registered_parsers.remove(parser_n_callback)

    def __call__(self, value):
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
    TimeStampedRegexParser(RX_TARGET_END, EVT_TARGET_END),

    # User state events
    TimeStampedRegexParser(RX_CONNECTED, EVT_CONNECTED),
    TimeStampedRegexParser(RX_DISCONNECTED, EVT_DISCONNECTED),
    TimeStampedRegexParser(RX_WENT_TO_MENU, EVT_WENT_TO_MENU),
    PositionedRegexParser(RX_SELECTED_ARMY, EVT_SELECTED_ARMY),

    # Aircraft events
    TimeStampedRegexParser(RX_WEAPONS_LOADED, EVT_WEAPONS_LOADED),
    PositionedRegexParser(RX_IN_FLIGHT, EVT_IN_FLIGHT),
    PositionedRegexParser(RX_CRASHED, EVT_CRASHED),
    PositionedRegexParser(RX_LANDED, EVT_LANDED),

    PositionedRegexParser(RX_DAMAGED_ON_GROUND, EVT_DAMAGED_ON_GROUND),
    PositionedRegexParser(RX_DAMAGED_SELF, EVT_DAMAGED_SELF),
    VictimOfUserRegexParser(RX_DAMAGED_BY_EAIR, EVT_DAMAGED_BY_EAIR),

    PositionedRegexParser(RX_SHOT_DOWN_SELF, EVT_SHOT_DOWN_SELF),
    VictimOfUserRegexParser(
        RX_SHOT_DOWN_BY_EAIR, EVT_SHOT_DOWN_BY_EAIR),
    VictimOfStaticRegexParser(
        RX_SHOT_DOWN_BY_STATIC, EVT_SHOT_DOWN_BY_STATIC),

    # Crew member events
    SeatRegexParser(RX_SEAT_OCCUPIED, EVT_SEAT_OCCUPIED),

    SeatRegexParser(RX_KILLED, EVT_KILLED),
    SeatVictimOfUserRegexParser(RX_KILLED_BY_EAIR, EVT_KILLED_BY_EAIR),

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
