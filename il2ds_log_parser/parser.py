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
        self.register(DateStampedRegexParser(RX_MISSION_PLAYING, EVT_MISSION_PLAYING))
        self.register(RegexParser(RX_MISSION_BEGIN, EVT_MISSION_BEGIN))
        self.register(RegexParser(RX_MISSION_END, EVT_MISSION_END))


default_log_parser = DefaultMultipleParser()
