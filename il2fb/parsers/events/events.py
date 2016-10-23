# coding: utf-8

import abc
import functools
import six

from il2fb.commons.structures import BaseStructure

from . import rx, tx
from .constants import TARGET_STATES
from .l10n import translations


_ = translations.ugettext_lazy


class Event(six.with_metaclass(abc.ABCMeta, BaseStructure)):
    """
    Base event structure.

    """
    transformers = tuple()

    def __init__(self, **kwargs):
        for key in self.__slots__:
            setattr(self, key, kwargs.get(key))
        super(Event, self).__init__()

    @property
    def name(self):
        return self.__class__.__name__

    @abc.abstractproperty
    def verbose_name(self):
        """
        Human-readable name of event.

        """

    @abc.abstractproperty
    def matcher(self):
        """
        A callable for matching strings.

        """

    def to_primitive(self, context=None):
        primitive = super(Event, self).to_primitive(context)
        primitive.update({
            'name': self.name,
            'verbose_name': six.text_type(self.verbose_name),
        })
        return primitive

    @classmethod
    def from_s(cls, s):
        match = cls.matcher(s)

        if match:
            data = cls.transform(match.groupdict())
            return cls(**data)

    @classmethod
    def transform(cls, data):
        for transformer in cls.transformers:
            transformer(data)
        return data

    def __repr__(self):
        return "<Event: {0}>".format(self.name)


class MissionIsPlaying(Event):
    """
    Example:

        "[Sep 15, 2013 8:33:05 PM] Mission: PH.mis is Playing"

    """
    __slots__ = ['date', 'time', 'mission', ]

    verbose_name = _("Mission is playing")
    matcher = rx.matcher(
        "{datetime}"  # 'datetime' regex group placeholder
        "Mission:"    #
        "\s"          # single whitespace
        "{mission}"   # 'mission' regex group placeholder
        "\s"          # single whitespace
        "is"          #
        "\s"          # single whitespace
        "Playing"     #
        "$"           # end of string
        .format(
            datetime=rx.DATE_TIME_GROUP_PREFIX,
            mission=rx.named_group('mission', ".+\.mis")
        )
    )
    transformers = (
        tx.transform_date,
        tx.transform_time,
    )


class MissionHasBegun(Event):
    """
    Example:

        "[8:33:05 PM] Mission BEGIN"

    """
    __slots__ = ['time', ]

    verbose_name = _("Mission has begun")
    matcher = rx.matcher(
        "{time}"   # 'time' regex group placeholder
        "Mission"  #
        "\s"       # single whitespace
        "BEGIN"    #
        "$"        # end of string
        .format(
            time=rx.TIME_GROUP_PREFIX,
        )
    )
    transformers = (
        tx.transform_time,
    )


class MissionHasEnded(Event):
    """
    Example:

        "[8:33:05 PM] Mission END"

    """
    __slots__ = ['time', ]

    verbose_name = _("Mission has ended")
    matcher = rx.matcher(
        "{time}"   # 'time' regex group placeholder
        "Mission"  #
        "\s"       # single whitespace
        "END"      #
        "$"        # end of string
        .format(
            time=rx.TIME_GROUP_PREFIX,
        )
    )
    transformers = (
        tx.transform_time,
    )


class MissionWasWon(Event):
    """
    Example:

        "[Sep 15, 2013 8:33:05 PM] Mission: RED WON"

    """
    __slots__ = ['date', 'time', 'belligerent', ]

    verbose_name = _("Mission was won")
    matcher = rx.matcher(
        "{datetime}"     # 'datetime' regex group placeholder
        "Mission:"       #
        "\s"             # single whitespace
        "{belligerent}"  # 'belligerent' regex group placeholder
        "\s"             # single whitespace
        "WON"            #
        "$"              # end of string
        .format(
            datetime=rx.DATE_TIME_GROUP_PREFIX,
            belligerent=rx.BELLIGERENT_GROUP,
        )
    )
    transformers = (
        tx.transform_date,
        tx.transform_time,
        tx.transform_belligerent,
    )


class TargetStateWasChanged(Event):
    """
    Example:

        "[8:33:05 PM] Target 3 Complete"

    """
    __slots__ = ['time', 'index', 'state', ]

    verbose_name = _("Target state was changed")
    STATES = TARGET_STATES
    matcher = rx.matcher(
        "{time}"   # 'time' regex group placeholder
        "Target"   #
        "\s"       # single whitespace
        "{index}"  # 'index' regex group placeholder
        "\s"       # single whitespace
        "{state}"  # 'state' regex group placeholder
        "$"        # end of string
        .format(
            time=rx.TIME_GROUP_PREFIX,
            index=rx.named_group('index', rx.NUMBER),
            state=rx.TARGET_STATE_GROUP,
        )
    )
    transformers = (
        tx.transform_time,
        functools.partial(tx.transform_int, field_name='index'),
    )


class HumanHasConnected(Event):
    """
    Example:

        "[8:33:05 PM] User0 has connected"

    """
    __slots__ = ['time', 'actor', ]

    verbose_name = _("Human has connected")
    matcher = rx.matcher(
        "{time}"     # 'time' regex group placeholder
        "{actor}"    # 'actor' regex group placeholder
        "\s"         # single whitespace
        "has"        #
        "\s"         # single whitespace
        "connected"  #
        "$"          # end of string
        .format(
            time=rx.TIME_GROUP_PREFIX,
            actor=rx.HUMAN_ACTOR_GROUP,
        )
    )
    transformers = (
        tx.transform_time,
        tx.human_as_actor,
    )


class HumanHasDisconnected(Event):
    """
    Example:

        "[8:33:05 PM] User0 has disconnected"

    """
    __slots__ = ['time', 'actor', ]

    verbose_name = _("Human has disconnected")
    matcher = rx.matcher(
        "{time}"        # 'time' regex group placeholder
        "{actor}"       # 'actor' regex group placeholder
        "\s"            # single whitespace
        "has"           #
        "\s"            # single whitespace
        "disconnected"  #
        "$"             # end of string
        .format(
            time=rx.TIME_GROUP_PREFIX,
            actor=rx.HUMAN_ACTOR_GROUP,
        )
    )
    transformers = (
        tx.transform_time,
        tx.human_as_actor,
    )


class HumanHasSelectedAirfield(Event):
    """
    Example:

        "[8:33:05 PM] User0 selected army Red at 100.0 200.99"

    """
    __slots__ = ['time', 'actor', 'belligerent', 'pos', ]

    verbose_name = _("Human has selected airfield")
    matcher = rx.matcher(
        "{time}"         # 'time' regex group placeholder
        "{actor}"        # 'actor' regex group placeholder
        "\s"             # single whitespace
        "selected"       #
        "\s"             # single whitespace
        "army"           #
        "\s"             # single whitespace
        "{belligerent}"  # 'belligerent' regex group placeholder
        "{pos}"          # 'pos' regex group placeholder
        .format(
            time=rx.TIME_GROUP_PREFIX,
            actor=rx.HUMAN_ACTOR_GROUP,
            belligerent=rx.BELLIGERENT_GROUP,
            pos=rx.POS_GROUP_SUFFIX,
        )
    )
    transformers = (
        tx.transform_time,
        tx.human_as_actor,
        tx.transform_belligerent,
        tx.transform_pos,
    )


class HumanAircraftHasSpawned(Event):
    """
    Example:

        "[8:33:05 PM] User0:Pe-8 loaded weapons '40fab100' fuel 40%"

    """
    __slots__ = ['time', 'actor', 'weapons', 'fuel', ]

    verbose_name = _("Human aircraft has spawned")
    matcher = rx.matcher(
        "{time}"     # 'time' regex group placeholder
        "{actor}"    # 'actor' regex group placeholder
        "\s"         # single whitespace
        "loaded"     #
        "\s"         # single whitespace
        "weapons"    #
        "\s"         # single whitespace
        "\'"         # opening single quote
        "{weapons}"  # 'weapons' regex group placeholder
        "\'"         # closing single quote
        "\s"         # single whitespace
        "fuel"       #
        "\s"         # single whitespace
        "{fuel}"     # 'fuel' regex group placeholder
        "%"          # percent sign
        "$"          # end of string
        .format(
            time=rx.TIME_GROUP_PREFIX,
            actor=rx.HUMAN_AIRCRAFT_ACTOR_GROUP,
            weapons=rx.named_group('weapons', rx.NON_WHITESPACES),
            fuel=rx.named_group('fuel', "\d{2,3}"),
        )
    )
    transformers = (
        tx.transform_time,
        tx.human_aircraft_as_actor,
        functools.partial(tx.transform_int, field_name='fuel'),
    )


class HumanHasWentToBriefing(Event):
    """
    Example:

        "[8:33:05 PM] User0 entered refly menu"

    """
    __slots__ = ['time', 'actor', ]

    verbose_name = _("Human has went to briefing")
    matcher = rx.matcher(
        "{time}"   # 'time' regex group placeholder
        "{actor}"  # 'actor' regex group placeholder
        "\s"       # single whitespace
        "entered"  #
        "\s"       # single whitespace
        "refly"    #
        "\s"       # single whitespace
        "menu"     #
        "$"        # end of string
        .format(
            time=rx.TIME_GROUP_PREFIX,
            actor=rx.HUMAN_ACTOR_GROUP,
        )
    )
    transformers = (
        tx.transform_time,
        tx.human_as_actor,
    )


class HumanHasToggledLandingLights(Event):
    """
    Example:

        "[8:33:05 PM] User0:Pe-8 turned landing lights off at 100.0 200.99"

    """
    __slots__ = ['time', 'actor', 'value', 'pos', ]

    verbose_name = _("Human has toggled landing lights")
    matcher = rx.matcher(
        "{time}"   # 'time' regex group placeholder
        "{actor}"  # 'actor' regex group placeholder
        "\s"       # single whitespace
        "turned"   #
        "\s"       # single whitespace
        "landing"  #
        "\s"       # single whitespace
        "lights"   #
        "\s"       # single whitespace
        "{value}"  # 'value' regex group placeholder
        "{pos}"    # 'pos' regex group placeholder
        .format(
            time=rx.TIME_GROUP_PREFIX,
            actor=rx.HUMAN_AIRCRAFT_ACTOR_GROUP,
            value=rx.TOGGLE_VALUE_GROUP,
            pos=rx.POS_GROUP_SUFFIX,
        )
    )
    transformers = (
        tx.transform_time,
        tx.human_aircraft_as_actor,
        tx.transform_pos,
    )


class HumanHasToggledWingtipSmokes(Event):
    """
    Example:

        "[8:33:05 PM] User0:Pe-8 turned wingtip smokes off at 100.0 200.99"

    """
    __slots__ = ['time', 'actor', 'value', 'pos', ]

    verbose_name = _("Human has toggled wingtip smokes")
    matcher = rx.matcher(
        "{time}"   # 'time' regex group placeholder
        "{actor}"  # 'actor' regex group placeholder
        "\s"       # single whitespace
        "turned"   #
        "\s"       # single whitespace
        "wingtip"  #
        "\s"       # single whitespace
        "smokes"   #
        "\s"       # single whitespace
        "{value}"  # 'value' regex group placeholder
        "{pos}"    # 'pos' regex group placeholder
        .format(
            time=rx.TIME_GROUP_PREFIX,
            actor=rx.HUMAN_AIRCRAFT_ACTOR_GROUP,
            value=rx.TOGGLE_VALUE_GROUP,
            pos=rx.POS_GROUP_SUFFIX,
        )
    )
    transformers = (
        tx.transform_time,
        tx.human_aircraft_as_actor,
        tx.transform_pos,
    )


class HumanHasChangedSeat(Event):
    """
    Example:

        "[8:33:05 PM] User0:Pe-8(0) seat occupied by User0 at 100.0 200.99"

    """
    __slots__ = ['time', 'actor', 'pos', ]

    verbose_name = _("Human has changed seat")
    matcher = rx.matcher(
        "{time}"      # 'time' regex group placeholder
        "{actor}"     # 'actor' regex group placeholder
        "\s"          # single whitespace
        "seat"        #
        "\s"          # single whitespace
        "occupied"    #
        "\s"          # single whitespace
        "by"          #
        "\s"          # single whitespace
        "{callsign}"  # 'callsign' regex placeholder
        "{pos}"       # 'pos' regex group placeholder
        .format(
            time=rx.TIME_GROUP_PREFIX,
            actor=rx.HUMAN_AIRCRAFT_CREW_MEMBER_ACTOR_GROUP,
            callsign=rx.CALLSIGN,
            pos=rx.POS_GROUP_SUFFIX,
        )
    )
    transformers = (
        tx.transform_time,
        tx.human_aircraft_crew_member_as_actor,
        tx.transform_pos,
    )


class HumanAircraftHasTookOff(Event):
    """
    Example:

        "[8:33:05 PM] User0:Pe-8 in flight at 100.0 200.99"

    """
    __slots__ = ['time', 'actor', 'pos', ]

    verbose_name = _("Human aircraft has took off")
    matcher = rx.matcher(
        "{time}"   # 'time' regex group placeholder
        "{actor}"  # 'actor' regex group placeholder
        "\s"       # single whitespace
        "in"       #
        "\s"       # single whitespace
        "flight"   #
        "{pos}"    # 'pos' regex group placeholder
        .format(
            time=rx.TIME_GROUP_PREFIX,
            actor=rx.HUMAN_AIRCRAFT_ACTOR_GROUP,
            pos=rx.POS_GROUP_SUFFIX,
        )
    )
    transformers = (
        tx.transform_time,
        tx.human_aircraft_as_actor,
        tx.transform_pos,
    )


class HumanAircraftHasLanded(Event):
    """
    Example:

        "[8:33:05 PM] User0:Pe-8 landed at 100.0 200.99"

    """
    __slots__ = ['time', 'actor', 'pos', ]

    verbose_name = _("Human aircraft has landed")
    matcher = rx.matcher(
        "{time}"   # 'time' regex group placeholder
        "{actor}"  # 'actor' regex group placeholder
        "\s"       # single whitespace
        "landed"   #
        "{pos}"    # 'pos' regex group placeholder
        .format(
            time=rx.TIME_GROUP_PREFIX,
            actor=rx.HUMAN_AIRCRAFT_ACTOR_GROUP,
            pos=rx.POS_GROUP_SUFFIX,
        )
    )
    transformers = (
        tx.transform_time,
        tx.human_aircraft_as_actor,
        tx.transform_pos,
    )


class HumanAircraftHasCrashed(Event):
    """
    Example:

        "[8:33:05 PM] User0:Pe-8 crashed at 100.0 200.99"

    """
    __slots__ = ['time', 'actor', 'pos', ]

    verbose_name = _("Human aircraft has crashed")
    matcher = rx.matcher(
        "{time}"   # 'time' regex group placeholder
        "{actor}"  # 'actor' regex group placeholder
        "\s"       # single whitespace
        "crashed"  #
        "{pos}"    # 'pos' regex group placeholder
        .format(
            time=rx.TIME_GROUP_PREFIX,
            actor=rx.HUMAN_AIRCRAFT_ACTOR_GROUP,
            pos=rx.POS_GROUP_SUFFIX,
        )
    )
    transformers = (
        tx.transform_time,
        tx.human_aircraft_as_actor,
        tx.transform_pos,
    )


class HumanHasDestroyedOwnAircraft(Event):
    """
    Examples:

        "[8:33:05 PM] User0:Pe-8 shot down by landscape at 100.0 200.99"
        "[8:33:05 PM] User0:Pe-8 shot down by NONAME at 100.0 200.99"

    """
    __slots__ = ['time', 'actor', 'pos', ]

    verbose_name = _("Human has destroyed own aircraft")
    matcher = rx.matcher(
        "{time}"     # 'time' regex group placeholder
        "{actor}"    # 'actor' regex group placeholder
        "\s"         # single whitespace
        "shot"       #
        "\s"         # single whitespace
        "down"       #
        "\s"         # single whitespace
        "by"         #
        "\s"         # single whitespace
        "{himself}"  # 'himself' regex placeholder
        "{pos}"      # 'pos' regex group placeholder
        .format(
            time=rx.TIME_GROUP_PREFIX,
            actor=rx.HUMAN_AIRCRAFT_ACTOR_GROUP,
            himself=rx.HIMSELF,
            pos=rx.POS_GROUP_SUFFIX,
        )
    )
    transformers = (
        tx.transform_time,
        tx.human_aircraft_as_actor,
        tx.transform_pos,
    )


class HumanHasDamagedOwnAircraft(Event):
    """
    Examples:

        "[8:33:05 PM] User0:Pe-8 damaged by landscape at 100.0 200.99"
        "[8:33:05 PM] User0:Pe-8 damaged by NONAME at 100.0 200.99"

    """
    __slots__ = ['time', 'actor', 'pos', ]

    verbose_name = _("Human has damaged own aircraft")
    matcher = rx.matcher(
        "{time}"     # 'time' regex group placeholder
        "{actor}"    # 'actor' regex group placeholder
        "\s"         # single whitespace
        "damaged"    #
        "\s"         # single whitespace
        "by"         #
        "\s"         # single whitespace
        "{himself}"  # 'himself' regex placeholder
        "{pos}"      # 'pos' regex group placeholder
        .format(
            time=rx.TIME_GROUP_PREFIX,
            actor=rx.HUMAN_AIRCRAFT_ACTOR_GROUP,
            himself=rx.HIMSELF,
            pos=rx.POS_GROUP_SUFFIX,
        )
    )
    transformers = (
        tx.transform_time,
        tx.human_aircraft_as_actor,
        tx.transform_pos,
    )


class HumanAircraftWasDamagedOnGround(Event):
    """
    Example:

        "[8:33:05 PM] User0:Pe-8 damaged on the ground at 100.0 200.99"

    """
    __slots__ = ['time', 'actor', 'pos', ]

    verbose_name = _("Human aircraft was damaged on the ground")
    matcher = rx.matcher(
        "{time}"   # 'time' regex group placeholder
        "{actor}"  # 'actor' regex group placeholder
        "\s"       # single whitespace
        "damaged"  #
        "\s"       # single whitespace
        "on"       #
        "\s"       # single whitespace
        "the"      #
        "\s"       # single whitespace
        "ground"   #
        "{pos}"    # 'pos' regex group placeholder
        .format(
            time=rx.TIME_GROUP_PREFIX,
            actor=rx.HUMAN_AIRCRAFT_ACTOR_GROUP,
            pos=rx.POS_GROUP_SUFFIX,
        )
    )
    transformers = (
        tx.transform_time,
        tx.human_aircraft_as_actor,
        tx.transform_pos,
    )


class HumanAircraftWasDamagedByHumanAircraft(Event):
    """
    Example:

        "[8:33:05 PM] User0:Pe-8 damaged by User1:Bf-109G-6_Late at 100.0 200.99"

    """
    __slots__ = ['time', 'actor', 'attacker', 'pos', ]

    verbose_name = _("Human aircraft was damaged by human aircraft")
    matcher = rx.matcher(
        "{time}"      # 'time' regex group placeholder
        "{actor}"     # 'actor' regex group placeholder
        "\s"          # single whitespace
        "damaged"     #
        "\s"          # single whitespace
        "by"          #
        "\s"          # single whitespace
        "{attacker}"  # 'attacker' regex group placeholder
        "{pos}"       # 'pos' regex group placeholder
        .format(
            time=rx.TIME_GROUP_PREFIX,
            actor=rx.HUMAN_AIRCRAFT_ACTOR_GROUP,
            attacker=rx.HUMAN_AIRCRAFT_ATTACKER_GROUP,
            pos=rx.POS_GROUP_SUFFIX,
        )
    )
    transformers = (
        tx.transform_time,
        tx.human_aircraft_as_actor,
        tx.human_aircraft_as_attacker,
        tx.transform_pos,
    )


class HumanAircraftWasDamagedByStationaryUnit(Event):
    """
    Example:

        "[8:33:05 PM] User0:Pe-8 damaged by 0_Static at 100.0 200.99"

    """
    __slots__ = ['time', 'actor', 'attacker', 'pos', ]

    verbose_name = _("Human aircraft was damaged by stationary unit")
    matcher = rx.matcher(
        "{time}"      # 'time' regex group placeholder
        "{actor}"     # 'actor' regex group placeholder
        "\s"          # single whitespace
        "damaged"     #
        "\s"          # single whitespace
        "by"          #
        "\s"          # single whitespace
        "{attacker}"  # 'attacker' regex group placeholder
        "{pos}"       # 'pos' regex group placeholder
        .format(
            time=rx.TIME_GROUP_PREFIX,
            actor=rx.HUMAN_AIRCRAFT_ACTOR_GROUP,
            attacker=rx.STATIONARY_UNIT_ATTACKER_GROUP,
            pos=rx.POS_GROUP_SUFFIX,
        )
    )
    transformers = (
        tx.transform_time,
        tx.human_aircraft_as_actor,
        tx.stationary_unit_as_attacker,
        tx.transform_pos,
    )


class HumanAircraftWasDamagedByAIAircraft(Event):
    """
    Example:

        "[8:33:05 PM] User0:Pe-8 damaged by r01000 at 100.0 200.99"

    """
    __slots__ = ['time', 'actor', 'attacker', 'pos', ]

    verbose_name = _("Human aircraft was damaged by AI aircraft")
    matcher = rx.matcher(
        "{time}"      # 'time' regex group placeholder
        "{actor}"     # 'actor' regex group placeholder
        "\s"          # single whitespace
        "damaged"     #
        "\s"          # single whitespace
        "by"          #
        "\s"          # single whitespace
        "{attacker}"  # 'attacker' regex group placeholder
        "{pos}"       # 'pos' regex group placeholder
        .format(
            time=rx.TIME_GROUP_PREFIX,
            actor=rx.HUMAN_AIRCRAFT_ACTOR_GROUP,
            attacker=rx.AI_AIRCRAFT_ATTACKER_GROUP,
            pos=rx.POS_GROUP_SUFFIX,
        )
    )
    transformers = (
        tx.transform_time,
        tx.human_aircraft_as_actor,
        tx.ai_aircraft_as_attacker,
        tx.transform_pos,
    )


class HumanAircraftWasShotDownByHumanAircraft(Event):
    """
    Example:

        "[8:33:05 PM] User0:Pe-8 shot down by User1:Bf-109G-6_Late at 100.0 200.99"

    """
    __slots__ = ['time', 'actor', 'attacker', 'pos', ]

    verbose_name = _("Human aircraft was shot down by human aircraft")
    matcher = rx.matcher(
        "{time}"      # 'time' regex group placeholder
        "{actor}"     # 'actor' regex group placeholder
        "\s"          # single whitespace
        "shot"        #
        "\s"          # single whitespace
        "down"        #
        "\s"          # single whitespace
        "by"          #
        "\s"          # single whitespace
        "{attacker}"  # 'attacker' regex group placeholder
        "{pos}"       # 'pos' regex group placeholder
        .format(
            time=rx.TIME_GROUP_PREFIX,
            actor=rx.HUMAN_AIRCRAFT_ACTOR_GROUP,
            attacker=rx.HUMAN_AIRCRAFT_ATTACKER_GROUP,
            pos=rx.POS_GROUP_SUFFIX,
        )
    )
    transformers = (
        tx.transform_time,
        tx.human_aircraft_as_actor,
        tx.human_aircraft_as_attacker,
        tx.transform_pos,
    )


class HumanAircraftWasShotDownByStationaryUnit(Event):
    """
    Example:

        "[8:33:05 PM] User0:Pe-8 shot down by 0_Static at 100.0 200.99"

    """
    __slots__ = ['time', 'actor', 'attacker', 'pos', ]

    verbose_name = _("Human aircraft was shot down by stationary unit")
    matcher = rx.matcher(
        "{time}"      # 'time' regex group placeholder
        "{actor}"     # 'actor' regex group placeholder
        "\s"          # single whitespace
        "shot"        #
        "\s"          # single whitespace
        "down"        #
        "\s"          # single whitespace
        "by"          #
        "\s"          # single whitespace
        "{attacker}"  # 'attacker' regex group placeholder
        "{pos}"       # 'pos' regex group placeholder
        .format(
            time=rx.TIME_GROUP_PREFIX,
            actor=rx.HUMAN_AIRCRAFT_ACTOR_GROUP,
            attacker=rx.STATIONARY_UNIT_ATTACKER_GROUP,
            pos=rx.POS_GROUP_SUFFIX,
        )
    )
    transformers = (
        tx.transform_time,
        tx.human_aircraft_as_actor,
        tx.stationary_unit_as_attacker,
        tx.transform_pos,
    )


class HumanAircraftWasShotDownByAIAircraft(Event):
    """
    Example:

        "[8:33:05 PM] User0:Pe-8 shot down by r01000 at 100.0 200.99"

    """
    __slots__ = ['time', 'actor', 'attacker', 'pos', ]

    verbose_name = _("Human aircraft was shot down by AI aircraft")
    matcher = rx.matcher(
        "{time}"      # 'time' regex group placeholder
        "{actor}"     # 'actor' regex group placeholder
        "\s"          # single whitespace
        "shot"        #
        "\s"          # single whitespace
        "down"        #
        "\s"          # single whitespace
        "by"          #
        "\s"          # single whitespace
        "{attacker}"  # 'attacker' regex group placeholder
        "{pos}"       # 'pos' regex group placeholder
        .format(
            time=rx.TIME_GROUP_PREFIX,
            actor=rx.HUMAN_AIRCRAFT_ACTOR_GROUP,
            attacker=rx.AI_AIRCRAFT_ATTACKER_GROUP,
            pos=rx.POS_GROUP_SUFFIX,
        )
    )
    transformers = (
        tx.transform_time,
        tx.human_aircraft_as_actor,
        tx.ai_aircraft_as_attacker,
        tx.transform_pos,
    )


class HumanAircraftCrewMemberHasBailedOut(Event):
    """
    Example:

        "[8:33:05 PM] User0:Pe-8(0) bailed out at 100.0 200.99"

    """
    __slots__ = ['time', 'actor', 'pos', ]

    verbose_name = _("Human aircraft crew member has bailed out")
    matcher = rx.matcher(
        "{time}"   # 'time' regex group placeholder
        "{actor}"  # 'actor' regex group placeholder
        "\s"       # single whitespace
        "bailed"   #
        "\s"       # single whitespace
        "out"      #
        "{pos}"    # 'pos' regex group placeholder
        .format(
            time=rx.TIME_GROUP_PREFIX,
            actor=rx.HUMAN_AIRCRAFT_CREW_MEMBER_ACTOR_GROUP,
            pos=rx.POS_GROUP_SUFFIX,
        )
    )
    transformers = (
        tx.transform_time,
        tx.human_aircraft_crew_member_as_actor,
        tx.transform_pos,
    )


class HumanAircraftCrewMemberHasLanded(Event):
    """
    Example:

        "[8:33:05 PM] User0:Pe-8(0) successfully bailed out at 100.0 200.99"

    """
    __slots__ = ['time', 'actor', 'pos', ]

    verbose_name = _("Human aircraft crew member has landed")
    matcher = rx.matcher(
        "{time}"        # 'time' regex group placeholder
        "{actor}"       # 'actor' regex group placeholder
        "\s"            # single whitespace
        "successfully"  #
        "\s"            # single whitespace
        "bailed"        #
        "\s"            # single whitespace
        "out"           #
        "{pos}"         # 'pos' regex group placeholder
        .format(
            time=rx.TIME_GROUP_PREFIX,
            actor=rx.HUMAN_AIRCRAFT_CREW_MEMBER_ACTOR_GROUP,
            pos=rx.POS_GROUP_SUFFIX,
        )
    )
    transformers = (
        tx.transform_time,
        tx.human_aircraft_crew_member_as_actor,
        tx.transform_pos,
    )


class HumanAircraftCrewMemberWasCaptured(Event):
    """
    Example:

        "[8:33:05 PM] User0:Pe-8(0) was captured at 100.0 200.99"

    """
    __slots__ = ['time', 'actor', 'pos', ]

    verbose_name = _("Human aircraft crew member was captured")
    matcher = rx.matcher(
        "{time}"    # 'time' regex group placeholder
        "{actor}"   # 'actor' regex group placeholder
        "\s"        # single whitespace
        "was"       #
        "\s"        # single whitespace
        "captured"  #
        "{pos}"     # 'pos' regex group placeholder
        .format(
            time=rx.TIME_GROUP_PREFIX,
            actor=rx.HUMAN_AIRCRAFT_CREW_MEMBER_ACTOR_GROUP,
            pos=rx.POS_GROUP_SUFFIX,
        )
    )
    transformers = (
        tx.transform_time,
        tx.human_aircraft_crew_member_as_actor,
        tx.transform_pos,
    )


class HumanAircraftCrewMemberWasWounded(Event):
    """
    Example:

        "[8:33:05 PM] User0:Pe-8(0) was wounded at 100.0 200.99"

    """
    __slots__ = ['time', 'actor', 'pos', ]

    verbose_name = _("Human aircraft crew member was wounded")
    matcher = rx.matcher(
        "{time}"   # 'time' regex group placeholder
        "{actor}"  # 'actor' regex group placeholder
        "\s"       # single whitespace
        "was"      #
        "\s"       # single whitespace
        "wounded"  #
        "{pos}"    # 'pos' regex group placeholder
        .format(
            time=rx.TIME_GROUP_PREFIX,
            actor=rx.HUMAN_AIRCRAFT_CREW_MEMBER_ACTOR_GROUP,
            pos=rx.POS_GROUP_SUFFIX,
        )
    )
    transformers = (
        tx.transform_time,
        tx.human_aircraft_crew_member_as_actor,
        tx.transform_pos,
    )


class HumanAircraftCrewMemberWasHeavilyWounded(Event):
    """
    Example:

        "[8:33:05 PM] User0:Pe-8(0) was heavily wounded at 100.0 200.99"

    """
    __slots__ = ['time', 'actor', 'pos', ]

    verbose_name = _("Human aircraft crew member was heavily wounded")
    matcher = rx.matcher(
        "{time}"   # 'time' regex group placeholder
        "{actor}"  # 'actor' regex group placeholder
        "\s"       # single whitespace
        "was"      #
        "\s"       # single whitespace
        "heavily"  #
        "\s"       # single whitespace
        "wounded"  #
        "{pos}"    # 'pos' regex group placeholder
        .format(
            time=rx.TIME_GROUP_PREFIX,
            actor=rx.HUMAN_AIRCRAFT_CREW_MEMBER_ACTOR_GROUP,
            pos=rx.POS_GROUP_SUFFIX,
        )
    )
    transformers = (
        tx.transform_time,
        tx.human_aircraft_crew_member_as_actor,
        tx.transform_pos,
    )


class HumanAircraftCrewMemberWasKilled(Event):
    """
    Example:

        "[8:33:05 PM] User0:Pe-8(0) was killed at 100.0 200.99"

    """
    __slots__ = ['time', 'actor', 'pos', ]

    verbose_name = _("Human aircraft crew member was killed")
    matcher = rx.matcher(
        "{time}"   # 'time' regex group placeholder
        "{actor}"  # 'actor' regex group placeholder
        "\s"       # single whitespace
        "was"      #
        "\s"       # single whitespace
        "killed"   #
        "{pos}"    # 'pos' regex group placeholder
        .format(
            time=rx.TIME_GROUP_PREFIX,
            actor=rx.HUMAN_AIRCRAFT_CREW_MEMBER_ACTOR_GROUP,
            pos=rx.POS_GROUP_SUFFIX,
        )
    )
    transformers = (
        tx.transform_time,
        tx.human_aircraft_crew_member_as_actor,
        tx.transform_pos,
    )


class HumanAircraftCrewMemberWasKilledByHumanAircraft(Event):
    """
    Example:

        "[8:33:05 PM] User0:Pe-8(0) was killed by User1:Bf-109G-6_Late at 100.0 200.99"

    """
    __slots__ = ['time', 'actor', 'attacker', 'pos', ]

    verbose_name = _("Human aircraft crew member was killed by human aircraft")
    matcher = rx.matcher(
        "{time}"      # 'time' regex group placeholder
        "{actor}"     # 'actor' regex group placeholder
        "\s"          # single whitespace
        "was"         #
        "\s"          # single whitespace
        "killed"      #
        "\s"          # single whitespace
        "by"          #
        "\s"          # single whitespace
        "{attacker}"  # 'attacker' regex group placeholder
        "{pos}"       # 'pos' regex group placeholder
        .format(
            time=rx.TIME_GROUP_PREFIX,
            actor=rx.HUMAN_AIRCRAFT_CREW_MEMBER_ACTOR_GROUP,
            attacker=rx.HUMAN_AIRCRAFT_ATTACKER_GROUP,
            pos=rx.POS_GROUP_SUFFIX,
        )
    )
    transformers = (
        tx.transform_time,
        tx.human_aircraft_crew_member_as_actor,
        tx.human_aircraft_as_attacker,
        tx.transform_pos,
    )


class HumanAircraftCrewMemberWasKilledByStationaryUnit(Event):
    """
    Example:

        "[8:33:05 PM] User0:Pe-8(0) was killed by 0_Static at 100.0 200.99"

    """
    __slots__ = ['time', 'actor', 'attacker', 'pos', ]

    verbose_name = _("Human aircraft crew member was killed by stationary unit")
    matcher = rx.matcher(
        "{time}"      # 'time' regex group placeholder
        "{actor}"     # 'actor' regex group placeholder
        "\s"          # single whitespace
        "was"         #
        "\s"          # single whitespace
        "killed"      #
        "\s"          # single whitespace
        "by"          #
        "\s"          # single whitespace
        "{attacker}"  # 'attacker' regex group placeholder
        "{pos}"       # 'pos' regex group placeholder
        .format(
            time=rx.TIME_GROUP_PREFIX,
            actor=rx.HUMAN_AIRCRAFT_CREW_MEMBER_ACTOR_GROUP,
            attacker=rx.STATIONARY_UNIT_ATTACKER_GROUP,
            pos=rx.POS_GROUP_SUFFIX,
        )
    )
    transformers = (
        tx.transform_time,
        tx.human_aircraft_crew_member_as_actor,
        tx.stationary_unit_as_attacker,
        tx.transform_pos,
    )


class BuildingWasDestroyedByHumanAircraft(Event):
    """
    Examples:

        "[8:33:05 PM] 3do/Buildings/Finland/CenterHouse1_w/live.sim destroyed by User0:Pe-8 at 100.0 200.99"
        "[8:33:05 PM] 3do/Buildings/Russia/Piter/House3_W/mono.sim destroyed by User1:Pe-8 at 300.0 400.99"

    """
    __slots__ = ['time', 'actor', 'attacker', 'pos', ]

    verbose_name = _("Building was destroyed by human aircraft")
    matcher = rx.matcher(
        "{time}"      # 'time' regex group placeholder
        "{actor}"     # 'actor' regex group placeholder
        "\s"          # single whitespace
        "destroyed"   #
        "\s"          # single whitespace
        "by"          #
        "\s"          # single whitespace
        "{attacker}"  # 'attacker' regex group placeholder
        "{pos}"       # 'pos' regex group placeholder
        .format(
            time=rx.TIME_GROUP_PREFIX,
            actor=rx.BUILDING_ACTOR_GROUP,
            attacker=rx.HUMAN_AIRCRAFT_ATTACKER_GROUP,
            pos=rx.POS_GROUP_SUFFIX,
        )
    )
    transformers = (
        tx.transform_time,
        tx.building_as_actor,
        tx.human_aircraft_as_attacker,
        tx.transform_pos,
    )


class BuildingWasDestroyedByStationaryUnit(Event):
    """
    Examples:

        "[8:33:05 PM] 3do/Buildings/Finland/CenterHouse1_w/live.sim destroyed by 0_Static at 100.0 200.99"
        "[8:33:05 PM] 3do/Buildings/Russia/Piter/House3_W/mono.sim destroyed by 1_Static at 300.0 400.99"

    """
    __slots__ = ['time', 'actor', 'attacker', 'pos', ]

    verbose_name = _("Building was destroyed by stationary unit")
    matcher = rx.matcher(
        "{time}"      # 'time' regex group placeholder
        "{actor}"     # 'actor' regex group placeholder
        "\s"          # single whitespace
        "destroyed"   #
        "\s"          # single whitespace
        "by"          #
        "\s"          # single whitespace
        "{attacker}"  # 'attacker' regex group placeholder
        "{pos}"       # 'pos' regex group placeholder
        .format(
            time=rx.TIME_GROUP_PREFIX,
            actor=rx.BUILDING_ACTOR_GROUP,
            attacker=rx.STATIONARY_UNIT_ATTACKER_GROUP,
            pos=rx.POS_GROUP_SUFFIX,
        )
    )
    transformers = (
        tx.transform_time,
        tx.building_as_actor,
        tx.stationary_unit_as_attacker,
        tx.transform_pos,
    )


class BuildingWasDestroyedByMovingUnit(Event):
    """
    Examples:

        "[8:33:05 PM] 3do/Buildings/Finland/CenterHouse1_w/live.sim destroyed by 0_Chief at 100.0 200.99"
        "[8:33:05 PM] 3do/Buildings/Russia/Piter/House3_W/mono.sim destroyed by 1_Chief at 300.0 400.99"

    """
    __slots__ = ['time', 'actor', 'attacker', 'pos', ]

    verbose_name = _("Building was destroyed by moving unit")
    matcher = rx.matcher(
        "{time}"      # 'time' regex group placeholder
        "{actor}"     # 'actor' regex group placeholder
        "\s"          # single whitespace
        "destroyed"   #
        "\s"          # single whitespace
        "by"          #
        "\s"          # single whitespace
        "{attacker}"  # 'attacker' regex group placeholder
        "{pos}"       # 'pos' regex group placeholder
        .format(
            time=rx.TIME_GROUP_PREFIX,
            actor=rx.BUILDING_ACTOR_GROUP,
            attacker=rx.MOVING_UNIT_ATTACKER_GROUP,
            pos=rx.POS_GROUP_SUFFIX,
        )
    )
    transformers = (
        tx.transform_time,
        tx.building_as_actor,
        tx.moving_unit_as_attacker,
        tx.transform_pos,
    )


class BuildingWasDestroyedByAIAircraft(Event):
    """
    Examples:

        "[8:33:05 PM] 3do/Buildings/Finland/CenterHouse1_w/live.sim destroyed by r01000 at 100.0 200.99"
        "[8:33:05 PM] 3do/Buildings/Russia/Piter/House3_W/mono.sim destroyed by r01001 at 300.0 400.99"

    """
    __slots__ = ['time', 'actor', 'attacker', 'pos', ]

    verbose_name = _("Building was destroyed by AI aircraft")
    matcher = rx.matcher(
        "{time}"      # 'time' regex group placeholder
        "{actor}"     # 'actor' regex group placeholder
        "\s"          # single whitespace
        "destroyed"   #
        "\s"          # single whitespace
        "by"          #
        "\s"          # single whitespace
        "{attacker}"  # 'attacker' regex group placeholder
        "{pos}"       # 'pos' regex group placeholder
        .format(
            time=rx.TIME_GROUP_PREFIX,
            actor=rx.BUILDING_ACTOR_GROUP,
            attacker=rx.AI_AIRCRAFT_ATTACKER_GROUP,
            pos=rx.POS_GROUP_SUFFIX,
        )
    )
    transformers = (
        tx.transform_time,
        tx.building_as_actor,
        tx.ai_aircraft_as_attacker,
        tx.transform_pos,
    )


class TreeWasDestroyedByHumanAircraft(Event):
    """
    Examples:

        "[8:33:05 PM] 3do/Tree/Line_W/live.sim destroyed by User0:Pe-8 at 100.0 200.99"
        "[8:33:05 PM] 3do/Tree/Line_W/mono.sim destroyed by User0:Pe-8 at 100.0 200.99"

    """
    __slots__ = ['time', 'attacker', 'pos', ]

    verbose_name = _("Tree was destroyed by human aircraft")
    matcher = rx.matcher(
        "{time}"      # 'time' regex group placeholder
        "{tree}"      # 'actor' regex group placeholder
        "\s"          # single whitespace
        "destroyed"   #
        "\s"          # single whitespace
        "by"          #
        "\s"          # single whitespace
        "{attacker}"  # 'attacker' regex group placeholder
        "{pos}"       # 'pos' regex group placeholder
        .format(
            time=rx.TIME_GROUP_PREFIX,
            tree=rx.TREE,
            attacker=rx.HUMAN_AIRCRAFT_ATTACKER_GROUP,
            pos=rx.POS_GROUP_SUFFIX,
        )
    )
    transformers = (
        tx.transform_time,
        tx.human_aircraft_as_attacker,
        tx.transform_pos,
    )


class TreeWasDestroyedByStationaryUnit(Event):
    """
    Examples:

        "[8:33:05 PM] 3do/Tree/Line_W/live.sim destroyed by 0_Static at 100.0 200.99"
        "[8:33:05 PM] 3do/Tree/Line_W/mono.sim destroyed by 0_Static at 100.0 200.99"

    """
    __slots__ = ['time', 'attacker', 'pos', ]

    verbose_name = _("Tree was destroyed by stationary unit")
    matcher = rx.matcher(
        "{time}"      # 'time' regex group placeholder
        "{tree}"      # 'actor' regex group placeholder
        "\s"          # single whitespace
        "destroyed"   #
        "\s"          # single whitespace
        "by"          #
        "\s"          # single whitespace
        "{attacker}"  # 'attacker' regex group placeholder
        "{pos}"       # 'pos' regex group placeholder
        .format(
            time=rx.TIME_GROUP_PREFIX,
            tree=rx.TREE,
            attacker=rx.STATIONARY_UNIT_ATTACKER_GROUP,
            pos=rx.POS_GROUP_SUFFIX,
        )
    )
    transformers = (
        tx.transform_time,
        tx.stationary_unit_as_attacker,
        tx.transform_pos,
    )


class TreeWasDestroyedByAIAircraft(Event):
    """
    Examples:

        "[8:33:05 PM] 3do/Tree/Line_W/live.sim destroyed by r01000 at 100.0 200.99"
        "[8:33:05 PM] 3do/Tree/Line_W/mono.sim destroyed by r01001 at 100.0 200.99"

    """
    __slots__ = ['time', 'attacker', 'pos', ]

    verbose_name = _("Tree was destroyed by AI aircraft")
    matcher = rx.matcher(
        "{time}"      # 'time' regex group placeholder
        "{tree}"      # 'actor' regex group placeholder
        "\s"          # single whitespace
        "destroyed"   #
        "\s"          # single whitespace
        "by"          #
        "\s"          # single whitespace
        "{attacker}"  # 'attacker' regex group placeholder
        "{pos}"       # 'pos' regex group placeholder
        .format(
            time=rx.TIME_GROUP_PREFIX,
            tree=rx.TREE,
            attacker=rx.AI_AIRCRAFT_ATTACKER_GROUP,
            pos=rx.POS_GROUP_SUFFIX,
        )
    )
    transformers = (
        tx.transform_time,
        tx.ai_aircraft_as_attacker,
        tx.transform_pos,
    )


class TreeWasDestroyed(Event):
    """
    Examples:

        "[8:33:05 PM] 3do/Tree/Line_W/live.sim destroyed by at 100.0 200.99"
        "[8:33:05 PM] 3do/Tree/Line_W/mono.sim destroyed by at 100.0 200.99"

    """
    __slots__ = ['time', 'pos', ]

    verbose_name = _("Tree was destroyed")
    matcher = rx.matcher(
        "{time}"     # 'time' regex group placeholder
        "{tree}"     # 'actor' regex group placeholder
        "\s"         # single whitespace
        "destroyed"  #
        "\s"         # single whitespace
        "by"         #
        "{pos}"      # 'pos' regex group placeholder
        .format(
            time=rx.TIME_GROUP_PREFIX,
            tree=rx.TREE,
            pos=rx.POS_GROUP_SUFFIX,
        )
    )
    transformers = (
        tx.transform_time,
        tx.transform_pos,
    )


class StationaryUnitWasDestroyed(Event):
    """
    Example:

        "[8:33:05 PM] 0_Static crashed at 100.0 200.99"

    """
    __slots__ = ['time', 'actor', 'pos', ]

    verbose_name = _("Stationary unit was destroyed")
    matcher = rx.matcher(
        "{time}"   # 'time' regex group placeholder
        "{actor}"  # 'actor' regex group placeholder
        "\s"       # single whitespace
        "crashed"  #
        "{pos}"    # 'pos' regex group placeholder
        .format(
            time=rx.TIME_GROUP_PREFIX,
            actor=rx.STATIONARY_UNIT_ACTOR_GROUP,
            pos=rx.POS_GROUP_SUFFIX,
        )
    )
    transformers = (
        tx.transform_time,
        tx.stationary_unit_as_actor,
        tx.transform_pos,
    )


class StationaryUnitWasDestroyedByStationaryUnit(Event):
    """
    Example:

        "[8:33:05 PM] 0_Static destroyed by 1_Static at 100.0 200.99"

    """
    __slots__ = ['time', 'actor', 'attacker', 'pos', ]

    verbose_name = _("Stationary unit was destroyed by stationary unit")
    matcher = rx.matcher(
        "{time}"      # 'time' regex group placeholder
        "{actor}"     # 'actor' regex group placeholder
        "\s"          # single whitespace
        "destroyed"   #
        "\s"          # single whitespace
        "by"          #
        "\s"          # single whitespace
        "{attacker}"  # 'attacker' regex group placeholder
        "{pos}"       # 'pos' regex group placeholder
        .format(
            time=rx.TIME_GROUP_PREFIX,
            actor=rx.STATIONARY_UNIT_ACTOR_GROUP,
            attacker=rx.STATIONARY_UNIT_ATTACKER_GROUP,
            pos=rx.POS_GROUP_SUFFIX,
        )
    )
    transformers = (
        tx.transform_time,
        tx.stationary_unit_as_actor,
        tx.stationary_unit_as_attacker,
        tx.transform_pos,
    )


class StationaryUnitWasDestroyedByMovingUnit(Event):
    """
    Example:

        "[8:33:05 PM] 0_Static destroyed by 0_Chief at 100.0 200.99"

    """
    __slots__ = ['time', 'actor', 'attacker', 'pos', ]

    verbose_name = _("Stationary unit was destroyed by moving unit")
    matcher = rx.matcher(
        "{time}"      # 'time' regex group placeholder
        "{actor}"     # 'actor' regex group placeholder
        "\s"          # single whitespace
        "destroyed"   #
        "\s"          # single whitespace
        "by"          #
        "\s"          # single whitespace
        "{attacker}"  # 'attacker' regex group placeholder
        "{pos}"       # 'pos' regex group placeholder
        .format(
            time=rx.TIME_GROUP_PREFIX,
            actor=rx.STATIONARY_UNIT_ACTOR_GROUP,
            attacker=rx.MOVING_UNIT_ATTACKER_GROUP,
            pos=rx.POS_GROUP_SUFFIX,
        )
    )
    transformers = (
        tx.transform_time,
        tx.stationary_unit_as_actor,
        tx.moving_unit_as_attacker,
        tx.transform_pos,
    )
