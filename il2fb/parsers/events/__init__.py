# -*- coding: utf-8 -*-

import six
import sys

from .exceptions import EventParsingError
from .grammar.events import event as _event_grammar
from .structures.events import *


def parse_string(string):
    try:
        return _event_grammar.parseString(string).event
    except Exception:
        error_type, original_msg, traceback = sys.exc_info()
        new_msg = ("{0} in string \"{1}\": {2}"
                   .format(error_type.__name__, string, original_msg))
        error = EventParsingError(new_msg)
        six.reraise(EventParsingError, error, traceback)
