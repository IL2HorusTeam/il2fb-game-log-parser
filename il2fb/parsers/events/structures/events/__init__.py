# -*- coding: utf-8 -*-

from il2fb.parsers.events.utils import translations

from .mixins import (
    EventWithTime, EventWithDateTime, EventWithBelligerent, EventWithCallsign,
    EventWithPos, EventWithActor, EventWithToggleValue, EventWithAggressor,
    EventWithVictim, EventWithAircraft,
)

__all__ = (
    'AIAircraftHasDespawned', 'AIAircraftWasDamagedOnGround',
    'AIHasDamagedHisAircraft',
    'BridgeWasDestroyedByHumanAircraft', 'BuildingWasDestroyedByHumanAircraft',
    'HumanAircraftWasDamagedByHumanAircraft',
    'HumanAircraftWasDamagedByStatic', 'HumanAircraftWasDamagedOnGround',
    'HumanAircraftWasShotDownByHumanAircraft',
    'HumanAircraftWasShotDownByStatic', 'HumanCrewMemberHasBailedOut',
    'HumanCrewMemberHasTouchedDown', 'HumanCrewMemberWasCaptured',
    'HumanCrewMemberWasHeavilyWounded', 'HumanCrewMemberWasKilled',
    'HumanCrewMemberWasKilledByHumanAircraft', 'HumanCrewMemberWasWounded',
    'HumanHasChangedSeat', 'HumanHasDestroyedHisAircraft', 'HumanHasConnected',
    'HumanAircraftHasCrashed', 'HumanHasDamagedHisAircraft',
    'HumanHasDisconnected', 'HumanAircraftHasLanded',
    'HumanHasSelectedAirfield', 'HumanAircraftHasSpawned',
    'HumanHasToggledLandingLights', 'HumanHasToggledWingtipSmokes',
    'HumanAircraftHasTookOff', 'HumanHasWentToBriefing', 'MissionHasBegun',
    'MissionHasEnded', 'MissionIsPlaying', 'MissionWasWon',
    'StaticWasDestroyed', 'StaticWasDestroyedByHumanAircraft',
    'TargetStateWasChanged', 'TreeWasDestroyedByHumanAircraft',
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
        return "<Event '{0}'>".format(self.name)

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


class TargetStateWasChanged(EventWithTime, Event):
    """
    Example::

        "[8:33:05 PM] Target 3 Complete"
    """
    verbose_name = _("Target state was changed")

    def __init__(self, **kwargs):
        super(TargetStateWasChanged, self).__init__(**kwargs)
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


class HumanAircraftHasSpawned(EventWithTime, EventWithActor, Event):
    """
    Example::

        "[8:33:05 PM] User0:Pe-8 loaded weapons '40fab100' fuel 40%"
    """
    verbose_name = _("Human aircraft has spawned")

    def __init__(self, **kwargs):
        super(HumanAircraftHasSpawned, self).__init__(**kwargs)
        self.weapons = kwargs['weapons']
        self.fuel = kwargs['fuel']


class HumanAircraftHasTookOff(EventWithTime,
                              EventWithActor,
                              EventWithPos,
                              Event):
    """
    Example::

        "[8:33:05 PM] User0:Pe-8 in flight at 100.0 200.99"
    """
    verbose_name = _("Human aircraft has took off")


class HumanAircraftHasLanded(EventWithTime,
                             EventWithActor,
                             EventWithPos,
                             Event):
    """
    Example::

        "[8:33:05 PM] User0:Pe-8 landed at 100.0 200.99"
    """
    verbose_name = _("Human aircraft has landed")


class HumanAircraftHasCrashed(EventWithTime,
                              EventWithVictim,
                              EventWithPos,
                              Event):
    """
    Example::

        "[8:33:05 PM] User0:Pe-8 crashed at 100.0 200.99"
    """
    verbose_name = _("Human aircraft has crashed")


class HumanHasDestroyedHisAircraft(EventWithTime,
                                   EventWithVictim,
                                   EventWithPos,
                                   Event):
    """
    Example::

        "[8:33:05 PM] User0:Pe-8 shot down by landscape at 100.0 200.99"
    """
    verbose_name = _("Human has destroyed his aircraft")


class HumanHasDamagedHisAircraft(EventWithTime,
                                 EventWithVictim,
                                 EventWithPos,
                                 Event):
    """
    Examples::

        "[8:33:05 PM] User0:Pe-8 damaged by landscape at 100.0 200.99"
        "[8:33:05 PM] User0:Pe-8 damaged by NONAME at 100.0 200.99"
    """
    verbose_name = _("Human has damaged his aircraft")


class HumanAircraftWasDamagedOnGround(EventWithTime,
                                      EventWithVictim,
                                      EventWithPos,
                                      Event):
    """
    Example::

        "[8:33:05 PM] User0:Pe-8 damaged on the ground at 100.0 200.99"
    """
    verbose_name = _("Human aircraft was damaged on ground")


class HumanAircraftWasDamagedByHumanAircraft(EventWithTime,
                                             EventWithVictim,
                                             EventWithAggressor,
                                             EventWithPos,
                                             Event):
    """
    Example::

        "[8:33:05 PM] User0:Pe-8 damaged by User1:Bf-109G-6_Late at 100.0 200.99"
    """
    verbose_name = _("Human aircraft was damaged by human aircraft")


class HumanAircraftWasDamagedByStatic(EventWithTime,
                                      EventWithVictim,
                                      EventWithAggressor,
                                      EventWithPos,
                                      Event):
    """
    Example::

        "[8:33:05 PM] User0:Pe-8 damaged by 0_Static at 100.0 200.99"
    """
    verbose_name = _("Human aircraft was damaged by static")


class HumanAircraftWasShotDownByHumanAircraft(EventWithTime,
                                              EventWithVictim,
                                              EventWithAggressor,
                                              EventWithPos,
                                              Event):
    """
    Example::

        "[8:33:05 PM] User0:Pe-8 shot down by User1:Bf-109G-6_Late at 100.0 200.99"
    """
    verbose_name = _("Human aircraft was shot down by human aircraft")


class HumanAircraftWasShotDownByStatic(EventWithTime,
                                       EventWithVictim,
                                       EventWithAggressor,
                                       EventWithPos,
                                       Event):
    """
    Example::

        "[8:33:05 PM] User0:Pe-8 shot down by 0_Static at 100.0 200.99"
    """
    verbose_name = _("Human aircraft was shot down by static")


class HumanCrewMemberHasBailedOut(EventWithTime,
                                  EventWithActor,
                                  EventWithPos,
                                  Event):
    """
    Example::

        "[8:33:05 PM] User0:Pe-8(0) bailed out at 100.0 200.99"
    """
    verbose_name = _("Human crew member has bailed out")


class HumanCrewMemberHasTouchedDown(EventWithTime,
                                    EventWithActor,
                                    EventWithPos,
                                    Event):
    """
    Example::

        "[8:33:05 PM] User0:Pe-8(0) successfully bailed out at 100.0 200.99"
    """
    verbose_name = _("Human crew member has touched down")


class HumanCrewMemberWasCaptured(EventWithTime,
                                 EventWithVictim,
                                 EventWithPos,
                                 Event):
    """
    Example::

        "[8:33:05 PM] User0:Pe-8(0) was captured at 100.0 200.99"
    """
    verbose_name = _("Human crew member was captured")


class HumanCrewMemberWasWounded(EventWithTime,
                                EventWithVictim,
                                EventWithPos,
                                Event):
    """
    Example::

        "[8:33:05 PM] User0:Pe-8(0) was wounded at 100.0 200.99"
    """
    verbose_name = _("Human crew member was wounded")


class HumanCrewMemberWasHeavilyWounded(EventWithTime,
                                       EventWithVictim,
                                       EventWithPos,
                                       Event):
    """
    Example::

        "[8:33:05 PM] User0:Pe-8(0) was heavily wounded at 100.0 200.99"
    """
    verbose_name = _("Human crew member was heavily wounded")


class HumanCrewMemberWasKilled(EventWithTime,
                               EventWithVictim,
                               EventWithPos,
                               Event):
    """
    Example::

        "[8:33:05 PM] User0:Pe-8(0) was killed at 100.0 200.99"
    """
    verbose_name = _("Human crew member was killed")


class HumanCrewMemberWasKilledByHumanAircraft(EventWithTime,
                                              EventWithVictim,
                                              EventWithAggressor,
                                              EventWithPos,
                                              Event):
    """
    Example::

        "[8:33:05 PM] User0:Pe-8(0) was killed by User1:Bf-109G-6_Late at 100.0 200.99"
    """
    verbose_name = _("Human crew member was killed by human aircraft")


class BuildingWasDestroyedByHumanAircraft(EventWithTime,
                                          EventWithVictim,
                                          EventWithAggressor,
                                          EventWithPos,
                                          Event):
    """
    Examples::

        "[8:33:05 PM] 3do/Buildings/Finland/CenterHouse1_w/live.sim destroyed by User0:Pe-8 at 100.0 200.99"
        "[8:33:05 PM] 3do/Buildings/Russia/Piter/House3_W/live.sim destroyed by User1:Pe-8 at 300.0 400.99"
    """
    verbose_name = _("Building was destroyed by human aircraft")


class TreeWasDestroyedByHumanAircraft(EventWithTime,
                                      EventWithAggressor,
                                      EventWithPos,
                                      Event):
    """
    Example::

        "[8:33:05 PM] 3do/Tree/Line_W/live.sim destroyed by User0:Pe-8 at 100.0 200.99"
    """
    verbose_name = _("Tree was destroyed by human aircraft")


class StaticWasDestroyed(EventWithTime,
                         EventWithVictim,
                         EventWithPos,
                         Event):
    """
    Example::

        "[8:33:05 PM] 0_Static crashed at 100.0 200.99"
    """
    verbose_name = _("Static was destroyed")


class StaticWasDestroyedByHumanAircraft(EventWithTime,
                                        EventWithVictim,
                                        EventWithAggressor,
                                        EventWithPos,
                                        Event):
    """
    Example::

        "[8:33:05 PM] 0_Static destroyed by User0:Pe-8 at 100.0 200.99"
    """
    verbose_name = _("Static was destroyed by human aircraft")


class BridgeWasDestroyedByHumanAircraft(EventWithTime,
                                        EventWithVictim,
                                        EventWithAggressor,
                                        EventWithPos,
                                        Event):
    """
    Example::

        "[8:33:05 PM]  Bridge0 destroyed by User0:Pe-8 at 100.0 200.99"

    Yes, there are 2 spaces before `Bridge0`.
    """
    verbose_name = _("Bridge was destroyed by human aircraft")


class AIAircraftHasDespawned(EventWithTime,
                             EventWithAircraft,
                             EventWithPos,
                             Event):
    """
    Example::

        "[8:33:05 PM] Pe-8 removed at 100.0 200.99"
    """
    verbose_name = _("AI aircraft has despawned")


class AIAircraftWasDamagedOnGround(EventWithTime,
                                   EventWithVictim,
                                   EventWithPos,
                                   Event):
    """
    Example::

        "[8:33:05 PM] Pe-8 damaged on the ground at 100.0 200.99"
    """
    verbose_name = _("AI aircraft was damaged on ground")


class AIHasDamagedHisAircraft(EventWithTime,
                              EventWithVictim,
                              EventWithPos,
                              Event):
    """
    Examples::

        "[8:33:05 PM] Pe-8 damaged by landscape at 100.0 200.99"
        "[8:33:05 PM] Pe-8 damaged by NONAME at 100.0 200.99"
    """
    verbose_name = _("AI has damaged his aircraft")
