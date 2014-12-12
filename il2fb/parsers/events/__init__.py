# -*- coding: utf-8 -*-

from .grammar.events import event


parse_string = lambda x: event.parseString(x).event
