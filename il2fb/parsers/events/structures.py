# -*- coding: utf-8 -*-

from .constants import EVENT_TYPES


class Base(object):
    __slots__ = ()

    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return all([
            getattr(self, x) == getattr(other, x)
            for x in self.__slots__
        ])

    def __ne__(self, other):
        return not (self == other)

    def __hash__(self):
        return hash(tuple(
            getattr(self, x) for x in self.__slots__
        ))


class Point2D(Base):
    __slots__ = ['x', 'y', ]

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __repr__(self):
        return "<Point2D '{0};{1}'>".format(self.x, self.y)


class Event(Base):
    __slots__ = ['type', ]

    def __init__(self, type):
        self.type = type

    def __repr__(self):
        return "<Event '{0}'>".format(self.type.name)


class MissionPlaying(Event):
    __slots__ = Event.__slots__ + ['date', 'time', 'mission', ]

    def __init__(self, source):
        super(MissionPlaying, self).__init__(EVENT_TYPES.MISSION_PLAYING)

        self.date = source['date']
        self.time = source['time']
        self.mission = source['mission']


class MissionBegin(Event):
    __slots__ = Event.__slots__ + ['time', ]

    def __init__(self, source):
        super(MissionBegin, self).__init__(EVENT_TYPES.MISSION_BEGIN)

        self.time = source['time']


class MissionEnd(Event):
    __slots__ = Event.__slots__ + ['time', ]

    def __init__(self, source):
        super(MissionEnd, self).__init__(EVENT_TYPES.MISSION_END)

        self.time = source['time']
