# -*- coding: utf-8 -*-

from il2fb.parsers.events.utils import translations

from .mixins import (
    EventWithTime, EventWithDateTime, EventWithBelligerent, EventWithCallsign,
    EventWithPos, EventWithActor, EventWithToggleValue, EventWithAggressor,
    EventWithVictim,
)

__all__ = (
    'MissionIsPlaying', 'MissionHasBegun', 'MissionHasEnded', 'MissionWasWon',
    'TargetStateHasChanged', 'HumanHasConnected', 'HumanHasDisconnected',
    'HumanHasWentToBriefing', 'HumanHasSelectedAirfield', 'HumanHasSpawned',
    'HumanHasTookOff', 'HumanHasLanded', 'HumanHasCrashed',
    'HumanWasDamagedOnGround', 'HumanHasDamagedHimself',
    'HumanHasCommittedSuicide', 'HumanWasShotDownByHuman',
    'HumanWasShotDownByStatic', 'HumanHasToggledLandingLights',
    'HumanHasToggledWingtipSmokes', 'HumanHasChangedSeat',
    'HumanCrewMemberHasBailedOut', 'HumanCrewMemberHasOpenedParachute',
    'HumanCrewMemberWasCaptured', 'HumanCrewMemberWasWounded',
    'HumanCrewMemberWasHeavilyWounded', 'HumanCrewMemberWasKilled',
    'HumanCrewMemberWasKilledByHuman', 'HumanWasDamagedByHuman',
    'BuildingWasDestroyedByHuman', 'TreeWasDestroyedByHuman',
    'StaticWasDestroyedByHuman', 'BridgeWasDestroyedByHuman',
)

_ = translations.ugettext_lazy


class Event(object):
    """
    Base event structure.
    """

    def __init__(self, *args, **kwargs):
        super(Event, self).__init__()
        self.name = self.__class__.__name__

    def __repr__(self):
        return "<Event '{0}'>".format(self.__class__.__name__)

    @property
    def verbose_name(self):
        raise NotImplementedError


class MissionIsPlaying(EventWithDateTime, Event):
    """
    Example::

        "[Sep 15, 2013 8:33:05 PM] Mission: PH.mis is Playing"
    """
    verbose_name = _("Mission is playing")

    def __init__(self, **kwargs):
        super(MissionIsPlaying, self).__init__(**kwargs)
        self.mission = kwargs['mission']


class MissionHasBegun(EventWithTime, Event):
    """
    Example::

        "[8:33:05 PM] Mission BEGIN"
    """
    verbose_name = _("Mission has begun")


class MissionHasEnded(EventWithTime, Event):
    """
    Example::

        "[8:33:05 PM] Mission END"
    """
    verbose_name = _("Mission has ended")


class MissionWasWon(EventWithDateTime, EventWithBelligerent, Event):
    """
    Example::

        "[Sep 15, 2013 8:33:05 PM] Mission: RED WON"
    """
    verbose_name = _("Mission was won")


class TargetStateHasChanged(EventWithTime, Event):
    """
    Example::

        "[8:33:05 PM] Target 3 Complete"
    """
    verbose_name = _("Target state has changed")

    def __init__(self, **kwargs):
        super(TargetStateHasChanged, self).__init__(**kwargs)
        self.target_index = kwargs['target_index']
        self.state = kwargs['target_end_state']


class HumanHasConnected(EventWithTime, EventWithCallsign, Event):
    """
    Example::

        "[8:33:05 PM] User0 has connected"
    """
    verbose_name = _("Human has connected")


class HumanHasDisconnected(EventWithTime, EventWithCallsign, Event):
    """
    Example::

        "[8:33:05 PM] User0 has disconnected"
    """
    verbose_name = _("Human has disconnected")


class HumanHasWentToBriefing(EventWithTime, EventWithCallsign, Event):
    """
    Example::

        "[8:33:05 PM] User0 entered refly menu"
    """
    verbose_name = _("Human has went to briefing")


class HumanHasSelectedAirfield(EventWithTime,
                               EventWithCallsign,
                               EventWithBelligerent,
                               EventWithPos,
                               Event):
    """
    Example::

        "[8:33:05 PM] User0 selected army Red at 100.0 200.99"
    """
    verbose_name = _("Human has selected airfield")


class HumanHasSpawned(EventWithTime, EventWithActor, Event):
    """
    Example::

        "[8:33:05 PM] User0:Pe-8 loaded weapons '40fab100' fuel 40%"
    """
    verbose_name = _("Human has spawned")

    def __init__(self, **kwargs):
        super(HumanHasSpawned, self).__init__(**kwargs)
        self.weapons = kwargs['weapons']
        self.fuel = kwargs['fuel']


class HumanHasTookOff(EventWithTime, EventWithActor, EventWithPos, Event):
    """
    Example::

        "[8:33:05 PM] User0:Pe-8 in flight at 100.0 200.99"
    """
    verbose_name = _("Human has took off")


class HumanHasLanded(EventWithTime, EventWithActor, EventWithPos, Event):
    """
    Example::

        "[8:33:05 PM] User0:Pe-8 landed at 100.0 200.99"
    """
    verbose_name = _("Human has landed")


class HumanHasCrashed(EventWithTime, EventWithActor, EventWithPos, Event):
    """
    Example::

        "[8:33:05 PM] User0:Pe-8 crashed at 100.0 200.99"
    """
    verbose_name = _("Human has crashed")


class HumanWasDamagedOnGround(EventWithTime,
                              EventWithActor,
                              EventWithPos,
                              Event):
    """
    Example::

        "[8:33:05 PM] User0:Pe-8 damaged on the ground at 100.0 200.99"
    """
    verbose_name = _("Human was damaged on ground")


class HumanHasDamagedHimself(EventWithTime,
                             EventWithActor,
                             EventWithPos,
                             Event):
    """
    Examples::

        "[8:33:05 PM] User0:Pe-8 damaged by landscape at 100.0 200.99"
        "[8:33:05 PM] User0:Pe-8 damaged by NONAME at 100.0 200.99"
    """
    verbose_name = _("Human has damaged himself")


class HumanWasDamagedByHuman(EventWithTime,
                             EventWithVictim,
                             EventWithAggressor,
                             EventWithPos,
                             Event):
    """
    Example::

        "[8:33:05 PM] User0:Pe-8 damaged by User1:Bf-109G-6_Late at 100.0 200.99"
    """
    verbose_name = _("Human was damaged by human")


class HumanHasCommittedSuicide(EventWithTime,
                               EventWithActor,
                               EventWithPos,
                               Event):
    """
    Example::

        "[8:33:05 PM] User0:Pe-8 shot down by landscape at 100.0 200.99"
    """
    verbose_name = _("Human has committed suicide")


class HumanWasShotDownByHuman(EventWithTime,
                              EventWithVictim,
                              EventWithAggressor,
                              EventWithPos,
                              Event):
    """
    Example::

        "[8:33:05 PM] User0:Pe-8 shot down by User1:Bf-109G-6_Late at 100.0 200.99"
    """
    verbose_name = _("Human was shot down by human")


class HumanWasShotDownByStatic(EventWithTime,
                               EventWithVictim,
                               EventWithAggressor,
                               EventWithPos,
                               Event):
    """
    Example::

        "[8:33:05 PM] User0:Pe-8 shot down by 0_Static at 100.0 200.99"
    """
    verbose_name = _("Human was shot down by static")


class HumanHasToggledLandingLights(EventWithTime,
                                   EventWithActor,
                                   EventWithToggleValue,
                                   EventWithPos,
                                   Event):
    """
    Example::

        "[8:33:05 PM] User0:Pe-8 turned landing lights off at 100.0 200.99"
    """
    verbose_name = _("Human has toggled landing lights")


class HumanHasToggledWingtipSmokes(EventWithTime,
                                   EventWithActor,
                                   EventWithToggleValue,
                                   EventWithPos,
                                   Event):

    """
    Example::

        "[8:33:05 PM] User0:Pe-8 turned wingtip smokes off at 100.0 200.99"
    """
    verbose_name = _("Human has toggled wingtip smokes")


class HumanHasChangedSeat(EventWithTime,
                          EventWithActor,
                          EventWithPos,
                          Event):
    """
    Example::

        "[8:33:05 PM] User0:Pe-8(0) seat occupied by User0 at 100.0 200.99"
    """
    verbose_name = _("Human has changed seat")


class HumanCrewMemberHasBailedOut(EventWithTime,
                                  EventWithActor,
                                  EventWithPos,
                                  Event):
    """
    Example::

        "[8:33:05 PM] User0:Pe-8(0) bailed out at 100.0 200.99"
    """
    verbose_name = _("Human crew member has bailed out")


class HumanCrewMemberHasOpenedParachute(EventWithTime,
                                        EventWithActor,
                                        EventWithPos,
                                        Event):
    """
    Example::

        "[8:33:05 PM] User0:Pe-8(0) successfully bailed out at 100.0 200.99"
    """
    verbose_name = _("Human crew member has opened parachute")


class HumanCrewMemberWasCaptured(EventWithTime,
                                 EventWithActor,
                                 EventWithPos,
                                 Event):
    """
    Example::

        "[8:33:05 PM] User0:Pe-8(0) was captured at 100.0 200.99"
    """
    verbose_name = _("Human crew member was captured")


class HumanCrewMemberWasWounded(EventWithTime,
                                EventWithActor,
                                EventWithPos,
                                Event):
    """
    Example::

        "[8:33:05 PM] User0:Pe-8(0) was wounded at 100.0 200.99"
    """
    verbose_name = _("Human crew member was wounded")


class HumanCrewMemberWasHeavilyWounded(EventWithTime,
                                       EventWithActor,
                                       EventWithPos,
                                       Event):
    """
    Example::

        "[8:33:05 PM] User0:Pe-8(0) was heavily wounded at 100.0 200.99"
    """
    verbose_name = _("Human crew member was heavily wounded")


class HumanCrewMemberWasKilled(EventWithTime,
                               EventWithActor,
                               EventWithPos,
                               Event):
    """
    Example::

        "[8:33:05 PM] User0:Pe-8(0) was killed at 100.0 200.99"
    """
    verbose_name = _("Human crew member was killed")


class HumanCrewMemberWasKilledByHuman(EventWithTime,
                                      EventWithVictim,
                                      EventWithAggressor,
                                      EventWithPos,
                                      Event):
    """
    Example::

        "[8:33:05 PM] User0:Pe-8(0) was killed by User1:Bf-109G-6_Late at 100.0 200.99"
    """
    verbose_name = _("Human crew member was killed by human")


class BuildingWasDestroyedByHuman(EventWithTime,
                                  EventWithVictim,
                                  EventWithAggressor,
                                  EventWithPos,
                                  Event):
    """
    Examples::

        "[8:33:05 PM] 3do/Buildings/Finland/CenterHouse1_w/live.sim destroyed by User0:Pe-8 at 100.0 200.99"
        "[8:33:05 PM] 3do/Buildings/Russia/Piter/House3_W/live.sim destroyed by User1:Pe-8 at 300.0 400.99"
    """
    verbose_name = _("Building was destroyed by human")


class TreeWasDestroyedByHuman(EventWithTime,
                              EventWithAggressor,
                              EventWithPos,
                              Event):
    """
    Example::

        "[8:33:05 PM] 3do/Tree/Line_W/live.sim destroyed by User0:Pe-8 at 100.0 200.99"
    """
    verbose_name = _("Tree was destroyed by human")


class StaticWasDestroyedByHuman(EventWithTime,
                                EventWithVictim,
                                EventWithAggressor,
                                EventWithPos,
                                Event):
    """
    Example::

        "[8:33:05 PM] 0_Static destroyed by User0:Pe-8 at 100.0 200.99"
    """
    verbose_name = _("Static was destroyed by human")


class BridgeWasDestroyedByHuman(EventWithTime,
                                EventWithVictim,
                                EventWithAggressor,
                                EventWithPos,
                                Event):
    """
    Example::

        "[8:33:05 PM]  Bridge0 destroyed by User0:Pe-8 at 100.0 200.99"

    Yes, there are 2 spaces before `Bridge0`.
    """
    verbose_name = _("Bridge was destroyed by human")
