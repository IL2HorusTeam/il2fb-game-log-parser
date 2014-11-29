# -*- coding: utf-8 -*-

from .mixins import (
    EventWithTime, EventWithDateTime, EventWithBelligerent, EventWithCallsign,
    EventWithPos, EventWithActor, EventWithCrewMember, EventWithToggleValue,
    EventWithAggressor, EventWithVictim,
)


__all__ = (
    'MissionIsPlaying', 'MissionHasBegun', 'MissionHasEnded', 'MissionWasWon',
    'TargetStateHasChanged', 'HumanHasConnected', 'HumanHasDisconnected',
    'HumanHasWentToBriefing', 'HumanHasSelectedAirfield', 'HumanHasSpawned',
    'HumanHasTookOff', 'HumanHasCrashed', 'HumanHasToggledLandingLights',
    'HumanHasToggledWingtipSmokes', 'HumanHasChangedSeat',
    'HumanCrewMemberHasBailedOut', 'HumanCrewMemberHasOpenedParachute',
    'HumanCrewMemberWasCaptured', 'HumanCrewMemberWasWounded',
    'HumanCrewMemberWasHeavilyWounded', 'HumanCrewMemberWasKilled',
    'HumanCrewMemberWasKilledByHuman',
)


class Event(object):

    def __init__(self, *args, **kwargs):
        super(Event, self).__init__()

    def __repr__(self):
        return "<Event '{0}'>".format(self.__class__.__name__)


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


class HumanHasConnected(EventWithTime, EventWithCallsign, Event):
    pass


class HumanHasDisconnected(EventWithTime, EventWithCallsign, Event):
    pass


class HumanHasWentToBriefing(EventWithTime, EventWithCallsign, Event):
    pass


class HumanHasSelectedAirfield(EventWithTime,
                               EventWithCallsign,
                               EventWithBelligerent,
                               EventWithPos,
                               Event):
    pass


class HumanHasSpawned(EventWithTime, EventWithActor, Event):

    def __init__(self, **kwargs):
        super(HumanHasSpawned, self).__init__(**kwargs)
        self.weapons = kwargs['weapons']
        self.fuel = kwargs['fuel']


class HumanHasTookOff(EventWithTime, EventWithActor, EventWithPos, Event):
    pass


class HumanHasCrashed(EventWithTime, EventWithActor, EventWithPos, Event):
    pass


class HumanHasToggledLandingLights(EventWithTime,
                                   EventWithActor,
                                   EventWithToggleValue,
                                   EventWithPos,
                                   Event):
    pass


class HumanHasToggledWingtipSmokes(EventWithTime,
                                   EventWithActor,
                                   EventWithToggleValue,
                                   EventWithPos,
                                   Event):

    pass


class HumanHasChangedSeat(EventWithTime,
                          EventWithCrewMember,
                          EventWithPos,
                          Event):
    pass


class HumanCrewMemberHasBailedOut(EventWithTime,
                                  EventWithCrewMember,
                                  EventWithPos,
                                  Event):
    pass


class HumanCrewMemberHasOpenedParachute(EventWithTime,
                                        EventWithCrewMember,
                                        EventWithPos,
                                        Event):
    pass


class HumanCrewMemberWasCaptured(EventWithTime,
                                 EventWithCrewMember,
                                 EventWithPos,
                                 Event):
    pass


class HumanCrewMemberWasWounded(EventWithTime,
                                EventWithCrewMember,
                                EventWithPos,
                                Event):
    pass


class HumanCrewMemberWasHeavilyWounded(EventWithTime,
                                       EventWithCrewMember,
                                       EventWithPos,
                                       Event):
    pass


class HumanCrewMemberWasKilled(EventWithTime,
                               EventWithCrewMember,
                               EventWithPos,
                               Event):
    pass


class HumanCrewMemberWasKilledByHuman(EventWithTime,
                                      EventWithVictim,
                                      EventWithAggressor,
                                      EventWithPos,
                                      Event):
    pass
