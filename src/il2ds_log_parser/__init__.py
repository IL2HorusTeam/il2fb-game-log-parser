# -*- coding: utf-8 -*-

from il2ds_log_parser import converter
from il2ds_log_parser.parser import default_evt_parser, parse_log_lines

register = default_evt_parser.register
unregister = default_evt_parser.unregister
parse_evt = default_evt_parser
parse_log = parse_log_lines
