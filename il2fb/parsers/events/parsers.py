# -*- coding: utf-8 -*-

import six
import sys

from pyparsing import ParseException

from .exceptions import EventParsingError
from .grammar.events import rules


__all__ = ('parse_string', )


def parse_string(string):
    for rule in rules:
        try:
            return rule.parseString(string).event
        except ParseException:
            continue
        except (SystemExit, KeyboardInterrupt):
            raise
        except:
            error_type, original_msg, traceback = sys.exc_info()
            new_msg = ("{0} in string \"{1}\": {2}"
                       .format(error_type.__name__, string, original_msg))
            error = EventParsingError(new_msg)
            six.reraise(EventParsingError, error, traceback)

    raise EventParsingError("No grammar was found for string \"{0}\""
                            .format(string))
