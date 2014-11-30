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
    'HumanHasTookOff', 'HumanHasLanded', 'HumanHasCrashed',
    'HumanWasDamagedOnGround', 'HumanHasDamagedHimself',
    'HumanHasToggledLandingLights', 'HumanHasToggledWingtipSmokes',
    'HumanHasChangedSeat', 'HumanCrewMemberHasBailedOut',
    'HumanCrewMemberHasOpenedParachute', 'HumanCrewMemberWasCaptured',
    'HumanCrewMemberWasWounded', 'HumanCrewMemberWasHeavilyWounded',
    'HumanCrewMemberWasKilled', 'HumanCrewMemberWasKilledByHuman',
    'HumanWasDamagedByHuman',
)


class Event(object):
    """
    Base event structure.
    """

    def __init__(self, *args, **kwargs):
        super(Event, self).__init__()

    def __repr__(self):
        return "<Event '{0}'>".format(self.__class__.__name__)


class MissionIsPlaying(EventWithDateTime, Event):
    """
    Example::

        "[Sep 15, 2013 8:33:05 PM] Mission: PH.mis is Playing"
    """

    def __init__(self, **kwargs):
        super(MissionIsPlaying, self).__init__(**kwargs)
        self.mission = kwargs['mission']


class MissionHasBegun(EventWithTime, Event):
    """
    Example::

        "[8:33:05 PM] Mission BEGIN"
    """


class MissionHasEnded(EventWithTime, Event):
    """
    Example::

        "[8:33:05 PM] Mission END"
    """


class MissionWasWon(EventWithDateTime, EventWithBelligerent, Event):
    """
    Example::

        "[Sep 15, 2013 8:33:05 PM] Mission: RED WON"
    """


class TargetStateHasChanged(EventWithTime, Event):
    """
    Example::

        "[8:33:05 PM] Target 3 Complete"
    """

    def __init__(self, **kwargs):
        super(TargetStateHasChanged, self).__init__(**kwargs)
        self.target_index = kwargs['target_index']
        self.state = kwargs['target_end_state']


class HumanHasConnected(EventWithTime, EventWithCallsign, Event):
    """
    Example::

        "[8:33:05 PM] User0 has connected"
    """


class HumanHasDisconnected(EventWithTime, EventWithCallsign, Event):
    """
    Example::

        "[8:33:05 PM] User0 has disconnected"
    """


class HumanHasWentToBriefing(EventWithTime, EventWithCallsign, Event):
    """
    Example::

        "[8:33:05 PM] User0 entered refly menu"
    """


class HumanHasSelectedAirfield(EventWithTime,
                               EventWithCallsign,
                               EventWithBelligerent,
                               EventWithPos,
                               Event):
    """
    Example::

        "[8:33:05 PM] User0 selected army Red at 100.0 200.99"
    """


class HumanHasSpawned(EventWithTime, EventWithActor, Event):
    """
    Example::

        "[8:33:05 PM] User0:Pe-8 loaded weapons '40fab100' fuel 40%"
    """

    def __init__(self, **kwargs):
        super(HumanHasSpawned, self).__init__(**kwargs)
        self.weapons = kwargs['weapons']
        self.fuel = kwargs['fuel']


class HumanHasTookOff(EventWithTime, EventWithActor, EventWithPos, Event):
    """
    Example::

        "[8:33:05 PM] User0:Pe-8 in flight at 100.0 200.99"
    """


class HumanHasLanded(EventWithTime, EventWithActor, EventWithPos, Event):
    """
    Example::

        "[8:33:05 PM] User0:Pe-8 landed at 100.0 200.99"
    """


class HumanHasCrashed(EventWithTime, EventWithActor, EventWithPos, Event):
    """
    Example::

        "[8:33:05 PM] User0:Pe-8 crashed at 100.0 200.99"
    """


class HumanWasDamagedOnGround(EventWithTime,
                              EventWithActor,
                              EventWithPos,
                              Event):
    """
    Example::

        "[8:33:05 PM] User0:Pe-8 damaged on the ground at 100.0 200.99"
    """


class HumanHasDamagedHimself(EventWithTime,
                             EventWithActor,
                             EventWithPos,
                             Event):
    """
    Examples::

        "[8:33:05 PM] User0:Pe-8 damaged by landscape at 100.0 200.99"
        "[8:33:05 PM] User0:Pe-8 damaged by NONAME at 100.0 200.99"
    """


class HumanWasDamagedByHuman(EventWithTime,
                             EventWithVictim,
                             EventWithAggressor,
                             EventWithPos,
                             Event):
    """
    Example::

        "[8:33:05 PM] User0:Pe-8 damaged by User1:Bf-109G-6_Late at 100.0 200.99"
    """


class HumanHasToggledLandingLights(EventWithTime,
                                   EventWithActor,
                                   EventWithToggleValue,
                                   EventWithPos,
                                   Event):
    """
    Example::

        "[8:33:05 PM] User0:Pe-8 turned landing lights off at 100.0 200.99"
    """


class HumanHasToggledWingtipSmokes(EventWithTime,
                                   EventWithActor,
                                   EventWithToggleValue,
                                   EventWithPos,
                                   Event):

    """
    Example::

        "[8:33:05 PM] User0:Pe-8 turned wingtip smokes off at 100.0 200.99"
    """


class HumanHasChangedSeat(EventWithTime,
                          EventWithCrewMember,
                          EventWithPos,
                          Event):
    """
    Example::

        "[8:33:05 PM] User0:Pe-8(0) seat occupied by User0 at 100.0 200.99"
    """


class HumanCrewMemberHasBailedOut(EventWithTime,
                                  EventWithCrewMember,
                                  EventWithPos,
                                  Event):
    """
    Example::

        "[8:33:05 PM] User0:Pe-8(0) bailed out at 100.0 200.99"
    """


class HumanCrewMemberHasOpenedParachute(EventWithTime,
                                        EventWithCrewMember,
                                        EventWithPos,
                                        Event):
    """
    Example::

        "[8:33:05 PM] User0:Pe-8(0) successfully bailed out at 100.0 200.99"
    """


class HumanCrewMemberWasCaptured(EventWithTime,
                                 EventWithCrewMember,
                                 EventWithPos,
                                 Event):
    """
    Example::

        "[8:33:05 PM] User0:Pe-8(0) was captured at 100.0 200.99"
    """


class HumanCrewMemberWasWounded(EventWithTime,
                                EventWithCrewMember,
                                EventWithPos,
                                Event):
    """
    Example::

        "[8:33:05 PM] User0:Pe-8(0) was wounded at 100.0 200.99"
    """


class HumanCrewMemberWasHeavilyWounded(EventWithTime,
                                       EventWithCrewMember,
                                       EventWithPos,
                                       Event):
    """
    Example::

        "[8:33:05 PM] User0:Pe-8(0) was heavily wounded at 100.0 200.99"
    """


class HumanCrewMemberWasKilled(EventWithTime,
                               EventWithCrewMember,
                               EventWithPos,
                               Event):
    """
    Example::

        "[8:33:05 PM] User0:Pe-8(0) was killed at 100.0 200.99"
    """


class HumanCrewMemberWasKilledByHuman(EventWithTime,
                                      EventWithVictim,
                                      EventWithAggressor,
                                      EventWithPos,
                                      Event):
    """
    Example::

        "[8:33:05 PM] User0:Pe-8(0) was killed by User1:Bf-109G-6_Late at 100.0 200.99"
    """
