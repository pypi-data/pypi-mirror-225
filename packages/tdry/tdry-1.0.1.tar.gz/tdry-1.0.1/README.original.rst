tdry
=======

.. image:: https://builds.sr.ht/~whynothugo/tdry.svg
  :target: https://builds.sr.ht/~whynothugo/tdry
  :alt: CI status

.. image:: https://codecov.io/gh/pimutils/tdry/branch/main/graph/badge.svg
  :target: https://codecov.io/gh/pimutils/tdry
  :alt: Codecov coverage report

.. image:: https://readthedocs.org/projects/tdry/badge/
  :target: https://tdry.rtfd.org/
  :alt: documentation

.. image:: https://img.shields.io/pypi/v/tdry.svg
  :target: https://pypi.python.org/pypi/tdry
  :alt: version on pypi

.. image:: https://img.shields.io/pypi/l/tdry.svg
  :target: https://github.com/pimutils/tdry/blob/main/LICENCE
  :alt: licence

.. image:: https://img.shields.io/badge/code%20style-black-000000.svg
  :target: https://pypi.org/project/black/
  :alt: code style: black

tdry is a simple, standards-based, cli todo (aka: task) manager. Todos
are stored into `icalendar <https://tools.ietf.org/html/rfc5545>`_ files, which
means you can sync them via `CalDAV <http://en.wikipedia.org/wiki/CalDAV>`_
using, for example, `vdirsyncer <https://vdirsyncer.readthedocs.org/>`_.

tdry is now part of the ``pimutils`` project, and is hosted at `GitHub
<https://github.com/pimutils/tdry>`_.

tdry should run fine on any Unix-like OS. It's been tested on GNU/Linux,
BSD, and macOS.  We do not support windows, and very basic testing seems to
indicate it does not work.

Feel free to join the IRC channel: #pimutils on irc.libera.chat.

Features
--------

* Listing, editing and creating todos.
* Todos are read from individual ics files from the configured directory. This
  matches the `vdir <https://vdirsyncer.readthedocs.org/en/latest/vdir.html>`_
  specification.
* There's support for the most common TODO features for now (summary,
  description, location, due date and priority).
* tdry should run on any major operating system (except Windows).
* Unsupported fields may not be shown but are *never* deleted or altered.

Documentation
-------------

For detailed usage, configuration and contributing documentation, please
consult the latest version of the manual at readthedocs_.

.. _readthedocs: https://tdry.readthedocs.org/

LICENCE
-------

tdry is licensed under the ISC licence. See LICENCE for details.
