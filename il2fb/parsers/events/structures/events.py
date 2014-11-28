# -*- coding: utf-8 -*-


class Event(object):

    def __init__(self, *args, **kwargs):
        super(Event, self).__init__()

    def __repr__(self):
        return "<Event '{0}'>".format(self.__class__.__name__)


def mixin_for_attribute(attribute_name):

    class Mixin(object):

        def __init__(self, **kwargs):
            super(Mixin, self).__init__(**kwargs)
            value = kwargs[attribute_name]
            setattr(self, attribute_name, value)

    return Mixin


EventWithTime = mixin_for_attribute('time')
EventWithDate = mixin_for_attribute('date')
EventWithCallsign = mixin_for_attribute('callsign')
EventWithBelligerent = mixin_for_attribute('belligerent')
EventWithPos = mixin_for_attribute('pos')


class EventWithDateTime(EventWithDate, EventWithTime):
    pass


class MissionIsPlaying(EventWithDateTime, Event):

    def __init__(self, **kwargs):
        super(MissionIsPlaying, self).__init__(**kwargs)
        self.mission = kwargs['mission']


class MissionHasBegun(EventWithTime, Event):
    pass


class MissionHasEnded(EventWithTime, Event):
    pass


class MissionWasWon(EventWithDateTime, EventWithBelligerent, Event):
    pass


class TargetStateHasChanged(EventWithTime, Event):

    def __init__(self, **kwargs):
        super(TargetStateHasChanged, self).__init__(**kwargs)
        self.target_index = kwargs['target_index']
        self.state = kwargs['target_end_state']


class UserHasConnected(EventWithTime, EventWithCallsign, Event):
    pass


class UserHasDisconnected(EventWithTime, EventWithCallsign, Event):
    pass


class UserHasWentToMenu(EventWithTime, EventWithCallsign, Event):
    pass


class UserHasSelectedAirfield(EventWithTime,
                              EventWithCallsign,
                              EventWithBelligerent,
                              EventWithPos,
                              Event):
    pass
