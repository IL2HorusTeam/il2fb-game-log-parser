# -*- coding: utf-8 -*-

from .mixins import (
    EventWithTime, EventWithDateTime, EventWithBelligerent, EventWithCallsign,
    EventWithPos, EventWithPilot, EventWithCrewMember, EventWithToggleValue,
    EventWithAggressor, EventWithVictim,
)


__all__ = (
    'MissionIsPlaying', 'MissionHasBegun', 'MissionHasEnded', 'MissionWasWon',
    'TargetStateHasChanged', 'UserHasConnected', 'UserHasDisconnected',
    'UserHasWentToBriefing', 'UserHasSelectedAirfield', 'UserHasTookOff',
    'UserHasSpawned', 'UserHasChangedSeat', 'CrewMemberHasBailedOut',
    'CrewMemberHasOpenedParachute', 'UserHasToggledLandingLights',
    'UserHasToggledWingtipSmokes', 'CrewMemberWasWounded',
    'CrewMemberWasHeavilyWounded', 'CrewMemberWasKilled',
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


class UserHasConnected(EventWithTime, EventWithCallsign, Event):
    pass


class UserHasDisconnected(EventWithTime, EventWithCallsign, Event):
    pass


class UserHasWentToBriefing(EventWithTime, EventWithCallsign, Event):
    pass


class UserHasSelectedAirfield(EventWithTime,
                              EventWithCallsign,
                              EventWithBelligerent,
                              EventWithPos,
                              Event):
    pass


class UserHasTookOff(EventWithTime, EventWithPilot, EventWithPos, Event):
    pass


class UserHasSpawned(EventWithTime, EventWithPilot, Event):

    def __init__(self, **kwargs):
        super(UserHasSpawned, self).__init__(**kwargs)
        self.weapons = kwargs['weapons']
        self.fuel = kwargs['fuel']


class UserHasChangedSeat(EventWithTime,
                         EventWithCrewMember,
                         EventWithPos,
                         Event):
    pass


class CrewMemberHasBailedOut(EventWithTime,
                             EventWithCrewMember,
                             EventWithPos,
                             Event):
    pass


class CrewMemberHasOpenedParachute(EventWithTime,
                                   EventWithCrewMember,
                                   EventWithPos,
                                   Event):
    pass


class UserHasToggledLandingLights(EventWithTime,
                                  EventWithPilot,
                                  EventWithToggleValue,
                                  EventWithPos,
                                  Event):
    pass


class UserHasToggledWingtipSmokes(EventWithTime,
                                  EventWithPilot,
                                  EventWithToggleValue,
                                  EventWithPos,
                                  Event):

    pass


class CrewMemberWasWounded(EventWithTime,
                           EventWithCrewMember,
                           EventWithPos,
                           Event):
    pass


class CrewMemberWasHeavilyWounded(EventWithTime,
                                  EventWithCrewMember,
                                  EventWithPos,
                                  Event):
    pass


class CrewMemberWasKilled(EventWithTime,
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
