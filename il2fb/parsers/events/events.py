# coding: utf-8

import abc
import functools
import re
import six

from il2fb.commons.structures import BaseStructure

from . import rx, tx
from .constants import TARGET_END_STATES
from .l10n import translations


_ = translations.ugettext_lazy


def make_matcher(s):
    return re.compile(s, re.VERBOSE).match


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
    matcher = make_matcher(
        "{datetime_prefix}"  # 'datetime' group regex placeholder
        "Mission:"           #
        "\s"                 # single whitespace
        "(?P<mission>"       # 'mission' group start
        "    .+"             # one or more symbols (e.g. "test" or "dogfight/test")
        "    \.mis"          # mission file extension
        ")"                  # 'mission' group end
        "\s"                 # single whitespace
        "is"                 #
        "\s"                 # single whitespace
        "Playing"            #
        "$"                  # end of string
        .format(
            datetime_prefix=rx.DATE_TIME_PREFIX,
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
    matcher = make_matcher(
        "{time_prefix}"  # 'time' group regex placeholder
        "Mission"        #
        "\s"             # single whitespace
        "BEGIN"          #
        "$"              # end of string
        .format(
            time_prefix=rx.TIME_PREFIX,
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
    matcher = make_matcher(
        "{time_prefix}"  # 'time' group regex placeholder
        "Mission"        #
        "\s"             # single whitespace
        "END"            #
        "$"              # end of string
        .format(
            time_prefix=rx.TIME_PREFIX,
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
    matcher = make_matcher(
        "{datetime_prefix}"    # 'datetime' group regex placeholder
        "Mission:"             #
        "\s"                   # single whitespace
        "{belligerent_group}"  # 'belligerent' group regex placeholder
        "\s"                   # single whitespace
        "WON"                  #
        "$"                    # end of string
        .format(
            datetime_prefix=rx.DATE_TIME_PREFIX,
            belligerent_group=rx.BELLIGERENT_GROUP,
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
    __slots__ = ['time', 'target_index', 'state', ]

    verbose_name = _("Target state was changed")
    STATES = TARGET_END_STATES
    matcher = make_matcher(
        "{time_prefix}"      # 'time' group regex placeholder
        "Target"             #
        "\s"                 # single whitespace
        "(?P<target_index>"  # 'target_index' group start
        "    \d+"            # one or more digits
        ")"                  # 'target_index' group end
        "\s"                 # single whitespace
        "{state_group}"      # 'state' group regex placeholder
        "$"                  # end of string
        .format(
            time_prefix=rx.TIME_PREFIX,
            state_group=rx.TARGET_END_STATE_GROUP,
        )
    )
    transformers = (
        tx.transform_time,
        functools.partial(tx.transform_int, field_name='target_index'),
    )


class HumanHasConnected(Event):
    """
    Example:

        "[8:33:05 PM] User0 has connected"

    """
    __slots__ = ['time', 'callsign', ]

    verbose_name = _("Human has connected")
    matcher = make_matcher(
        "{time_prefix}"     # 'time' group regex placeholder
        "{callsign_group}"  # 'callsign' group regex placeholder
        "\s"                # single whitespace
        "has"               #
        "\s"                # single whitespace
        "connected"         #
        "$"                 # end of string
        .format(
            time_prefix=rx.TIME_PREFIX,
            callsign_group=rx.HUMAN_CALLSIGN_GROUP,
        )
    )
    transformers = (
        tx.transform_time,
    )


class HumanHasDisconnected(Event):
    """
    Example:

        "[8:33:05 PM] User0 has disconnected"

    """
    __slots__ = ['time', 'callsign', ]

    verbose_name = _("Human has disconnected")
    matcher = make_matcher(
        "{time_prefix}"     # 'time' group regex placeholder
        "{callsign_group}"  # 'callsign' group regex placeholder
        "\s"                # single whitespace
        "has"               #
        "\s"                # single whitespace
        "disconnected"      #
        "$"                 # end of string
        .format(
            time_prefix=rx.TIME_PREFIX,
            callsign_group=rx.HUMAN_CALLSIGN_GROUP,
        )
    )
    transformers = (
        tx.transform_time,
    )


class HumanHasSelectedAirfield(Event):
    """
    Example:

        "[8:33:05 PM] User0 selected army Red at 100.0 200.99"

    """
    __slots__ = ['time', 'callsign', 'belligerent', 'pos', ]

    verbose_name = _("Human has selected airfield")
    matcher = make_matcher(
        "{time_prefix}"        # 'time' group regex placeholder
        "{callsign_group}"     # 'callsign' group regex placeholder
        "\s"                   # single whitespace
        "selected"             #
        "\s"                   # single whitespace
        "army"                 #
        "\s"                   # single whitespace
        "{belligerent_group}"  # 'belligerent' group regex placeholder
        "{pos_suffix}"         # 'pos' group regex placeholder
        .format(
            time_prefix=rx.TIME_PREFIX,
            callsign_group=rx.HUMAN_CALLSIGN_GROUP,
            belligerent_group=rx.BELLIGERENT_GROUP,
            pos_suffix=rx.POS_SUFFIX,
        )
    )
    transformers = (
        tx.transform_time,
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
    matcher = make_matcher(
        "{time_prefix}"  # 'time' group regex placeholder
        "{actor_group}"  # 'actor' group regex placeholder
        "\s"             # single whitespace
        "loaded"         #
        "\s"             # single whitespace
        "weapons"        #
        "\s"             # single whitespace
        "\'"             # opening single quote
        "(?P<weapons>"   # 'weapons' group start
        "    \S+"        # one or more non-whitespace characters
        ")"              # 'weapons' group end
        "\'"             # closing single quote
        "\s"             # single whitespace
        "fuel"           #
        "\s"             # single whitespace
        "(?P<fuel>"      # 'fuel' group start
        "    \d{{2,3}}"  # 2 or 3 digits for fuel percentage
        ")"              # 'fuel' group end
        "%"              # percent sign
        "$"
        .format(
            time_prefix=rx.TIME_PREFIX,
            actor_group=rx.HUMAN_AIRCRAFT_GROUP,
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
    __slots__ = ['time', 'callsign', ]

    verbose_name = _("Human has went to briefing")
    matcher = make_matcher(
        "{time_prefix}"     # 'time' group regex placeholder
        "{callsign_group}"  # 'callsign' group regex placeholder
        "\s"                # single whitespace
        "entered"           #
        "\s"                # single whitespace
        "refly"             #
        "\s"                # single whitespace
        "menu"              #
        "$"                 # end of string
        .format(
            time_prefix=rx.TIME_PREFIX,
            callsign_group=rx.HUMAN_CALLSIGN_GROUP,
        )
    )
    transformers = (
        tx.transform_time,
    )


class HumanHasToggledLandingLights(Event):
    """
    Example:

        "[8:33:05 PM] User0:Pe-8 turned landing lights off at 100.0 200.99"

    """
    __slots__ = ['time', 'actor', 'value', 'pos', ]

    verbose_name = _("Human has toggled landing lights")
    matcher = make_matcher(
        "{time_prefix}"  # 'time' group regex placeholder
        "{actor_group}"  # 'actor' group regex placeholder
        "\s"             # single whitespace
        "turned"         #
        "\s"             # single whitespace
        "landing"        #
        "\s"             # single whitespace
        "lights"         #
        "\s"             # single whitespace
        "{value_group}"  # 'value' group regex placeholder
        "{pos_suffix}"   # 'pos' group regex placeholder
        .format(
            time_prefix=rx.TIME_PREFIX,
            actor_group=rx.HUMAN_AIRCRAFT_GROUP,
            value_group=rx.TOGGLE_VALUE_GROUP,
            pos_suffix=rx.POS_SUFFIX,
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
    matcher = make_matcher(
        "{time_prefix}"  # 'time' group regex placeholder
        "{actor_group}"  # 'actor' group regex placeholder
        "\s"             # single whitespace
        "turned"         #
        "\s"             # single whitespace
        "wingtip"        #
        "\s"             # single whitespace
        "smokes"         #
        "\s"             # single whitespace
        "{value_group}"  # 'value' group regex placeholder
        "{pos_suffix}"   # 'pos' group regex placeholder
        .format(
            time_prefix=rx.TIME_PREFIX,
            actor_group=rx.HUMAN_AIRCRAFT_GROUP,
            value_group=rx.TOGGLE_VALUE_GROUP,
            pos_suffix=rx.POS_SUFFIX,
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
    matcher = make_matcher(
        "{time_prefix}"  # 'time' group regex placeholder
        "{actor_group}"  # 'actor' group regex placeholder
        "\s"             # single whitespace
        "seat"           #
        "\s"             # single whitespace
        "occupied"       #
        "\s"             # single whitespace
        "by"             #
        "\s"             # single whitespace
        "{callsign}"     # 'callsign' regex placeholder
        "{pos_suffix}"   # 'pos' group regex placeholder
        .format(
            time_prefix=rx.TIME_PREFIX,
            actor_group=rx.HUMAN_AIRCRAFT_CREW_MEMBER_GROUP,
            callsign=rx.HUMAN_CALLSIGN,
            pos_suffix=rx.POS_SUFFIX,
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
    matcher = make_matcher(
        "{time_prefix}"  # 'time' group regex placeholder
        "{actor_group}"  # 'actor' group regex placeholder
        "\s"             # single whitespace
        "in"             #
        "\s"             # single whitespace
        "flight"         #
        "{pos_suffix}"   # 'pos' group regex placeholder
        .format(
            time_prefix=rx.TIME_PREFIX,
            actor_group=rx.HUMAN_AIRCRAFT_GROUP,
            pos_suffix=rx.POS_SUFFIX,
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
    matcher = make_matcher(
        "{time_prefix}"  # 'time' group regex placeholder
        "{actor_group}"  # 'actor' group regex placeholder
        "\s"             # single whitespace
        "landed"         #
        "{pos_suffix}"   # 'pos' group regex placeholder
        .format(
            time_prefix=rx.TIME_PREFIX,
            actor_group=rx.HUMAN_AIRCRAFT_GROUP,
            pos_suffix=rx.POS_SUFFIX,
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
    matcher = make_matcher(
        "{time_prefix}"  # 'time' group regex placeholder
        "{actor_group}"  # 'actor' group regex placeholder
        "\s"             # single whitespace
        "crashed"        #
        "{pos_suffix}"   # 'pos' group regex placeholder
        .format(
            time_prefix=rx.TIME_PREFIX,
            actor_group=rx.HUMAN_AIRCRAFT_GROUP,
            pos_suffix=rx.POS_SUFFIX,
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
    matcher = make_matcher(
        "{time_prefix}"  # 'time' group regex placeholder
        "{actor_group}"  # 'actor' group regex placeholder
        "\s"             # single whitespace
        "damaged"        #
        "\s"             # single whitespace
        "by"             #
        "\s"             # single whitespace
        "{himself}"      # 'himself' regex placeholder
        "{pos_suffix}"   # 'pos' group regex placeholder
        .format(
            time_prefix=rx.TIME_PREFIX,
            actor_group=rx.HUMAN_AIRCRAFT_GROUP,
            himself=rx.HIMSELF,
            pos_suffix=rx.POS_SUFFIX,
        )
    )
    transformers = (
        tx.transform_time,
        tx.human_aircraft_as_actor,
        tx.transform_pos,
    )
