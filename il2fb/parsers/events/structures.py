# -*- coding: utf-8 -*-


class Base(object):
    __slots__ = []

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


class Event(object):

    def __init__(self, *args, **kwargs):
        super(Event, self).__init__()

    @property
    def event_type(self):
        raise NotImplementedError

    def __repr__(self):
        return "<Event '{0}'>".format(self.event_type.name)


class EventWithTime(object):

    def __init__(self, data):
        super(EventWithTime, self).__init__(data)
        self.time = data['time']


class EventWithDate(object):

    def __init__(self, data):
        super(EventWithDate, self).__init__(data)
        self.date = data['date']


class MissionIsPlaying(EventWithDate, EventWithTime, Event):

    def __init__(self, data):
        super(MissionIsPlaying, self).__init__(data)
        self.mission = data['mission']


class MissionBegin(EventWithTime, Event):
    pass


class MissionEnd(EventWithTime, Event):
    pass
