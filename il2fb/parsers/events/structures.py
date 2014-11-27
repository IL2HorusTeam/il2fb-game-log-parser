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

    def __repr__(self):
        return "<Event '{0}'>".format(self.__class__.__name__)


class EventWithTime(object):

    def __init__(self, **kwargs):
        super(EventWithTime, self).__init__(**kwargs)
        self.time = kwargs['time']


class EventWithDate(object):

    def __init__(self, **kwargs):
        super(EventWithDate, self).__init__(**kwargs)
        self.date = kwargs['date']


class MissionIsPlaying(EventWithDate, EventWithTime, Event):

    def __init__(self, **kwargs):
        super(MissionIsPlaying, self).__init__(**kwargs)
        self.mission = kwargs['mission']


class MissionHasBegun(EventWithTime, Event):
    pass


class MissionHasEnded(EventWithTime, Event):
    pass


class MissionWasWon(EventWithDate, EventWithTime, Event):

    def __init__(self, **kwargs):
        super(MissionWasWon, self).__init__(**kwargs)
        self.belligerent = kwargs['belligerent']


class TargetStateHasChanged(EventWithTime, Event):

    def __init__(self, **kwargs):
        super(TargetStateHasChanged, self).__init__(**kwargs)
        self.target_index = kwargs['target_index']
        self.state = kwargs['target_end_state']
