=====================
IL-2 FB Events Parser
=====================

|pypi_package| |pypi_downloads| |python_versions| |docs| |license|

|unix_build| |windows_build| |coverage_status|

|code_issues| |codeclimate| |codacy| |quality| |health| |requirements|


L10N state:

|translations|


**Table of contents**

.. contents::
    :local:
    :depth: 1
    :backlinks: none


Synopsis
--------

This is a Python library which parses events from log file produced by
IL-2 FB Dedicated Server. Resulting information about events is stored in
special data structures.


Demo
----

You may see this library in action even if you do not understand its purpose.

All you need is just to `visit project's demo page`_.

That page allows you to test parser's ability to process some string. If you
do not know what to enter to the text area, you may ``Insert test data``
and parse it.

If something goes wrong, you will be prompted to confirm automatic creation of
bug report which will be
`listed on this page <https://github.com/IL2HorusTeam/il2fb-events-parser/issues>`_.


Known events
------------

This library supports the vast majority of events produced by dedicated
server.

To see their list, go to the `demo page`_ and click
``See the list of supported events`` link.

You may find `definitions of datastructures here <https://github.com/IL2HorusTeam/il2fb-events-parser/blob/master/il2fb/parsers/events/structures/events.py>`_
and you may `explore their internals here <https://github.com/IL2HorusTeam/il2fb-events-parser/blob/master/tests/test_events.py>`_.


Installation
------------

Get it from PyPI:

.. code-block:: bash

  pip install il2fb-events-parser


Usage
-----

Basic usage
~~~~~~~~~~~

If you need to be able to parse all events this library knows about, use
``parse_string()``:

.. code-block:: python

  from il2fb.parsers.events import parse_string
  event = parse_string("[8:33:05 PM] User0 has connected")
  print(event)
  # <Event 'HumanHasConnected'>
  event.time
  # datetime.time(20, 33, 5)
  event.callsign
  # 'User0'
  import pprint
  pprint.pprint(event.to_primitive())
  # {'callsign': 'User0',
  #  'name': 'HumanHasConnected',
  #  'time': '20:33:05',
  #  'verbose_name': u'Human has connected'}


Possible exceptions
~~~~~~~~~~~~~~~~~~~

Certain errors may be raised if you will try to parse unknown event or known
event with invalid data:

.. code-block:: python

  parse_string("foo bar")
  # Traceback (most recent call last):
  # ...
  # EventParsingError: No grammar was found for string "foo bar"
  parse_string("[99:99:99 PM] Mission BEGIN")
  # Traceback (most recent call last):
  # ...
  # ValueError: time data '99:99:99 PM' does not match format '%I:%M:%S %p'

Current list of supported events is rather full, but ``EventParsingError`` is
quite possible, because server's events are undocumented and this library may
do not know about all of them.

In case you need to catch this error, its full name is
``il2fb.parsers.events.exceptions.EventParsingError``.

Other errors such as ``ValueError`` are quite impossible if you are parsing log
created by dedicated server.


Safe usage
~~~~~~~~~~

You may use ``parse_string_safely()`` if you don't care about any exceptions:

.. code-block:: python

  from il2fb.parsers.events import parse_string_safely
  event = parse_string_safely("foo bar")
  event is None
  # True

Any error (except ``SystemExit`` and ``KeyboardInterrupt``) will be muted and
``None`` will be returned.


Tweaks
------

Each event has own grammar rule for parsing strings. Each rule increases max
time of parsing of a single string.

For example, this time equals to ~10 ms for Python 2.7.8 running under
Linux kernel 3.13 on Intel® Core™ i3-2120. Therefore, in the worst case you
will be able to parse 100 events per second.

This may not be an issue for you, but if it is, you may skip some events to
speed up parsing process.


Explicitly tell which events you are interested in
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

You may explicitly tell which events you are interested in, if you are not
interested in the vast majority of events supported by this library.

To do so, you will need to use ``InclusiveEventsParser``:

.. code-block:: python

  from il2fb.parsers.events import InclusiveEventsParser
  from il2fb.parsers.events import HumanHasConnected, HumanHasSelectedAirfield
  parser = InclusiveEventsParser([
      HumanHasConnected, HumanHasSelectedAirfield,
  ])
  parser.parse_string("[8:33:05 PM] User0 has connected")
  # <Event 'HumanHasConnected'>
  parser.parse_string("[8:33:05 PM] User0 selected army Red at 100.0 200.99")
  # <Event 'HumanHasSelectedAirfield'>
  parser.parse_string("[8:33:05 PM] User0 has disconnected")
  # None

Here, ``parse_string()`` method of our parser will work same way as
``parse_string_safely()`` function.


Explicitly tell which events you are NOT interested in
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

If you are not interested only in some events, you can exclude them using
``ExclusiveEventsParser``:


.. code-block:: python

  from il2fb.parsers.events import ExclusiveEventsParser
  from il2fb.parsers.events import (
      TreeWasDestroyed, TreeWasDestroyedByAIAircraft,
      TreeWasDestroyedByHumanAircraft, TreeWasDestroyedByStatic,
  )
  parser = ExclusiveEventsParser([
      TreeWasDestroyed, TreeWasDestroyedByAIAircraft,
      TreeWasDestroyedByHumanAircraft, TreeWasDestroyedByStatic,
  ])
  parser.parse_string("[8:33:05 PM] User0 has connected")
  # <Event 'HumanHasConnected'>
  parser.parse_string("[8:33:05 PM] 3do/Tree/Line_W/live.sim destroyed by User0:Pe-8 at 100.0 200.99")
  # None

Just like in case of ``InclusiveEventsParser``, ``parse_string()`` will work
same way as ``parse_string_safely()`` function.


Ideas for future
~~~~~~~~~~~~~~~~

Another way to speed up parsing is to use LRU cache for grammar rules.

Here, the key idea is that some types of events usually may come in sequence
during game flow. For example, user destroys a group of objects with bombs,
user changes seat in his aircraft rapidly, the whole crew bails out, etc.

It seems to be OK to use ``collections.deque`` to implement cache for such
situations.

The problem is that we need to preserve order of rules for events of similar
types. To do so, first of all, we need to group all existing rules. Then we
will need combine a group of rules into a single rule. This must be done during
instantiation of parser, because list of events we are interested in may vary
(see ``InclusiveEventsParser`` and ``ExclusiveEventsParser``).

This idea seems to be nice and useful, but maybe it's just a premature
optimization.


.. |unix_build| image:: https://travis-ci.org/IL2HorusTeam/il2fb-events-parser.svg?branch=master
   :target: https://travis-ci.org/IL2HorusTeam/il2fb-events-parser

.. |windows_build| image:: https://ci.appveyor.com/api/projects/status/a47k677tr59bd5wg/branch/master?svg=true
    :target: https://ci.appveyor.com/project/oblalex/il2fb-events-parser
    :alt: Build status of the master branch on Windows

.. |coverage_status| image:: http://codecov.io/github/IL2HorusTeam/il2fb-events-parser/coverage.svg?branch=master
    :target: http://codecov.io/github/IL2HorusTeam/il2fb-events-parser?branch=master
    :alt: Test coverage

.. |codeclimate| image:: https://codeclimate.com/github/IL2HorusTeam/il2fb-events-parser/badges/gpa.svg
   :target: https://codeclimate.com/github/IL2HorusTeam/il2fb-events-parser
   :alt: Code Climate

.. |codacy| image:: https://api.codacy.com/project/badge/c0385f01ffa545dea3a52a51cfc53221
    :target: https://www.codacy.com/app/oblalex/il2fb-events-parser
    :alt: Codacy Code Review

.. |quality| image:: https://scrutinizer-ci.com/g/IL2HorusTeam/il2fb-events-parser/badges/quality-score.png?b=master
   :target: https://scrutinizer-ci.com/g/IL2HorusTeam/il2fb-events-parser/?branch=master
   :alt: Scrutinizer Code Quality

.. |health| image:: https://landscape.io/github/IL2HorusTeam/il2fb-events-parser/master/landscape.svg?style=flat
   :target: https://landscape.io/github/IL2HorusTeam/il2fb-events-parser/master
   :alt: Code Health
   
.. |code_issues| image:: https://www.quantifiedcode.com/api/v1/project/49c826961bd54c14a5ca1959e07d05c1/badge.svg
     :target: https://www.quantifiedcode.com/app/project/49c826961bd54c14a5ca1959e07d05c1
     :alt: Code issues

.. |pypi_package| image:: http://img.shields.io/pypi/v/il2fb-events-parser.svg?style=flat
   :target: http://badge.fury.io/py/il2fb-events-parser/

.. |pypi_downloads| image:: http://img.shields.io/pypi/dm/il2fb-events-parser.svg?style=flat
   :target: https://crate.io/packages/il2fb-events-parser/

.. |python_versions| image:: https://img.shields.io/badge/Python-2.7,3.4-brightgreen.svg?style=flat
   :alt: Supported versions of Python

.. |docs| image:: https://readthedocs.org/projects/il2fb-events-parser/badge/?version=latest
    :target: https://readthedocs.org/projects/il2fb-events-parser/?badge=latest
    :alt: Documentation Status

.. |license| image:: https://img.shields.io/badge/license-LGPLv3-blue.svg?style=flat
   :target: https://github.com/IL2HorusTeam/il2fb-events-parser/blob/master/LICENSE

.. |requirements| image:: https://requires.io/github/IL2HorusTeam/il2fb-events-parser/requirements.svg?branch=master
     :target: https://requires.io/github/IL2HorusTeam/il2fb-events-parser/requirements/?branch=master
     :alt: Requirements Status

.. |translations| image:: https://www.transifex.com/projects/p/il2fb-events-parser/resource/il2fb-events-parserpo/chart/image_png
    :target: https://www.transifex.com/projects/p/il2fb-events-parser/
    :alt: Status of translations

.. _read the docs: http://il2fb-events-parser.readthedocs.org/

.. _demo page: http://il2horusteam.github.io/il2fb-events-parser/
.. _visit project's demo page: `demo page`_
