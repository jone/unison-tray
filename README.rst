=============
 unison-tray
=============

Provides a tray icon for the great `unison` file synchronizer.


Features
========

- A tray icon with idle, syncing and conflict states.
- Drop down menu, allowing to sync in background or in foreground (Terminal app).
- Detects file system changes with local root (read from `~/.unison/default.prf`) and
  automatically syncs (delayed).
- Syncs on application start.


Compatibility
=============

- Mac OS X (Tested with 10.6 and 10.7).
- python 2.7 with cocoa bindings, as installed on every compatible Mac OS X.


Installation
============

::

    $ git clone https://github.com/jone/unison-tray.git
    $ cd unison-tray
    $ /usr/bin/python2.7 bootstrap.py
    $ bin/buildout


Usage
=====

Be sure your unison configuration (``~/.unison/default.prf``) is configured so
that it works with only executing ``$ unison`` without root arguments.

You should create the initial copy before starting unison-tray, since unison
asks questions.

Start the tray icon from within the ``unison-tray`` directory with:

::

    $ bin/utray


License
=======

"THE BEER-WARE LICENSE" (Revision 42):

jone_ wrote this script. As long as you retain this notice you
can do whatever you want with this stuff. If we meet some day, and you think
this stuff is worth it, you can buy me a beer in return.


.. _unison: http://www.cis.upenn.edu/~bcpierce/unison
.. _jone: http://github.com/jone
