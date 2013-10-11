# -*- coding: utf-8 -*-

import datetime
import re

from il2ds_log_parser.constants import *
from il2ds_log_parser.regex import *


def parse_time(value):
    """Take time in format of 'H:MM:SS AM/PM' and convert it to ISO format"""
    dt = datetime.datetime.strptime(value, LOG_TIME_FORMAT)
    return dt.time().isoformat()


def parse_date(value):
    """Take date in format of 'Mon DD, YYYY' and convert it to ISO format"""
    dt = datetime.datetime.strptime(value, LOG_DATE_FORMAT)
    return dt.date().isoformat()


class RegexParser(object):

    def __init__(self, regex, evt_type):
        self.rx = re.compile(regex)
        self.evt_type = evt_type

    def __call__(self, value):
        m = self.rx.match(value)
        if m:
            result = m.groupdict()
            result['type'] = self.evt_type
            result['time'] = parse_time(result['time'])
            return result
        return None

    def __str__(self):
        return "{type}: {regex}".format(
            type=self.evt_type, regex=self.rx)

    def __unicode__(self):
        return unicode(self.__str__())


class DateStampedRegexParser(RegexParser):

    def __call__(self, value):
        result = super(DateStampedRegexParser, self).__call__(value)
        if result:
            result['date'] = parse_date(result['date'])
        return result


class PositionedRegexParser(RegexParser):

    def __call__(self, value):
        result = super(PositionedRegexParser, self).__call__(value)
        if result and 'pos_x' in result and 'pos_y' in result:
            x = result.pop('pos_x')
            y = result.pop('pos_y')
            result['pos'] = {
                'x': float(x),
                'y': float(y),
            }
        return result


class SeatRegexParser(PositionedRegexParser):

    def __call__(self, value):
        result = super(SeatRegexParser, self).__call__(value)
        if result:
            result['seat'] = int(result['seat'])
        return result


class RegistrationError(Exception):
    """Thrown when registering or unregistering goes wrong."""


class MultipleParser(object):

    def __init__(self):
        self._registered_parsers = []

    def is_registered(self, parser):
        return parser in self._registered_parsers

    def register(self, parser):
        if self.is_registered(parser):
            raise RegistrationError(
                "Parser is already registered: {parser}".format(parser=parser))
        self._registered_parsers.append(parser)

    def unregister(self, parser):
        if not self.is_registered(parser):
            raise RegistrationError(
                "Parser is not registered yet: {parser}".format(parser=parser))
        self._registered_parsers.remove(parser)

    def __call__(self, value):
        for parser in self._registered_parsers:
            result = parser(value)
            if result:
                return result
        return None


class DefaultMultipleParser(MultipleParser):

    def __init__(self):
        super(DefaultMultipleParser, self).__init__()
        self.register(SeatRegexParser(RX_SEAT_OCCUPIED, EVT_SEAT_OCCUPIED))
        self.register(PositionedRegexParser(RX_DESTROYED_BLD, EVT_DESTROYED))
        self.register(PositionedRegexParser(RX_DESTROYED_STATIC, EVT_DESTROYED))
        self.register(PositionedRegexParser(RX_LANDING_LIGHTS, EVT_LANDING_LIGHTS))
        self.register(PositionedRegexParser(RX_WINGTIP_SMOKES, EVT_WINGTIP_SMOKES))

        self.register(DateStampedRegexParser(RX_MISSION_PLAYING, EVT_MISSION_PLAYING))
        self.register(RegexParser(RX_MISSION_BEGIN, EVT_MISSION_BEGIN))
        self.register(RegexParser(RX_MISSION_END, EVT_MISSION_END))

        self.register(RegexParser(RX_CONNECTED, EVT_CONNECTED))
        self.register(RegexParser(RX_DISCONNECTED, EVT_DISCONNECTED))
        self.register(RegexParser(RX_WENT_TO_MENU, EVT_WENT_TO_MENU))

        self.register(RegexParser(RX_WEAPONS_LOADED, EVT_WEAPONS_LOADED))
        self.register(PositionedRegexParser(RX_SELECTED_ARMY, EVT_SELECTED_ARMY))
        self.register(PositionedRegexParser(RX_IN_FLIGHT, EVT_IN_FLIGHT))
        self.register(PositionedRegexParser(RX_CRASHED, EVT_CRASHED))
        self.register(PositionedRegexParser(RX_LANDED, EVT_LANDED))
        self.register(PositionedRegexParser(RX_DAMAGED_ON_GROUND, EVT_DAMAGED_ON_GROUND))
        self.register(PositionedRegexParser(RX_DAMAGED_SELF, EVT_DAMAGED_SELF))

        self.register(SeatRegexParser(RX_BAILED_OUT, EVT_BAILED_OUT))
        self.register(SeatRegexParser(RX_SUCCESSFULLY_BAILED_OUT, EVT_SUCCESSFULLY_BAILED_OUT))
        self.register(SeatRegexParser(RX_WOUNDED, EVT_WOUNDED))
        self.register(SeatRegexParser(RX_HEAVILY_WOUNDED, EVT_HEAVILY_WOUNDED))
        self.register(SeatRegexParser(RX_KILLED, EVT_KILLED))
        self.register(SeatRegexParser(RX_CAPTURED, EVT_CAPTURED))


default_evt_parser = DefaultMultipleParser()


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
        if "3do/Tree/Line_W" in line:
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
