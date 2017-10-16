# coding: utf-8
"""
Priorities are used to control order in which regular expressions are applied
to strings.

This is vital, because regular expressions for human-related events are
more specific than AI-related events, but less specific than other events.

Regular expressions for AI-related are the least specific and must be used at
the last turn.

The more priority number, the less important is event.

"""

DEFAULT = 0

AND_HUMAN = 1 << 0
AND_AI = 1 << 1

BY_HUMAN = 1 << 2
BY_AI = 1 << 3

HUMAN = 1 << 4
AI = 1 << 5


def get_event_priority(event_class):
    name = event_class.__name__
    priority = DEFAULT

    if name.startswith("Human"):
        priority |= HUMAN
    elif name.startswith("AI"):
        priority |= AI

    if "ByHuman" in name:
        priority |= BY_HUMAN
    elif "ByAI" in name:
        priority |= BY_AI

    if "AndHuman" in name:
        priority |= AND_HUMAN
    elif "AndAI" in name:
        priority |= AND_AI

    return priority
