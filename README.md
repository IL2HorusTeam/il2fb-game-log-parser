##IL-2 FB Dedicated Server Events Log Parser

[![Build Status](https://travis-ci.org/IL2HorusTeam/il2ds-log-parser.png?branch=master)](https://travis-ci.org/IL2HorusTeam/il2ds-log-parser)
[![Coverage Status](https://coveralls.io/repos/IL2HorusTeam/il2ds-log-parser/badge.png)](https://coveralls.io/r/IL2HorusTeam/il2ds-log-parser)
[![PyPi package](https://badge.fury.io/py/il2ds-log-parser.png)](http://badge.fury.io/py/il2ds-log-parser/)
[![Downloads](https://pypip.in/d/il2ds-log-parser/badge.png)](https://crate.io/packages/il2ds-log-parser/)

Parse log file of IL-2 FB DS and produce information about events.

Currently mostly all events can be parsed. AI-related events still need to be
studied, so that's why this is beta version.

Installation
------------

    pip install il2ds-log-parser

Usage
-----

### Parse single events from log:

    from il2ds_log_parser import parse_evt
    evt = parse_evt("[8:46:57 PM] User selected army Red at 238667.0 104506.0")

`evt` will contain:

    {
        'army': 'Red',
        'pos': {
            'y': 104506.0,
            'x': 238667.0
        },
        'callsign': 'User',
        'time': datetime.time(20, 46, 57),
        'type': 'SEL_ARMY',
    }

### Parse the whole log and group events by missions:

    from il2ds_log_parser import parse_log

    with open('/path/to/events.log', 'r') as f:
        lines = [line.strip() for line in f.readlines()]

    missions, unparsed = parse_log(lines)

### Convert the whole log to JSON and print statistics:

    python il2ds_log_parser/scripts/log2json.py --src=log_examples/Helsinki_event_eventlog.lst --dst=Helsinki_events.json
    Total: 3326.
    Done: 3326.
    Skipped: 0.

This will convert [Helsinki_event_eventlog.lst](log_examples/Helsinki_event_eventlog.lst) into [Helsinki_events.json](https://www.dropbox.com/s/3irqjk5p0jxf9yy/Helsinki_events.json).
