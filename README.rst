=============
 unison-tray
=============

Provides a tray icon for the great `unison`_ file synchronizer.


Features
========

- A tray icon with idle, syncing and conflict states.
- Drop down menu, allowing to sync in background or in foreground (Terminal app).
- Detects file system changes with local root (read from `~/.unison/default.prf`) and
  automatically syncs (delayed).
- Syncs periodically, configurable in ``syncer.cfg`` (default every 5 minutes).
- Syncs on application start.
- It just calls ``unison -batch`` (background) or ``unison -auto`` (foreground for
  conflict resolution). It does not configure unison in any other way.

.. image:: https://github.com/jone/unison-tray/raw/master/screenshot.png



Compatibility
=============

- Mac OS X (Tested on 10.9 Mavericks and 10.8.4 Mountain Lion)
- python 2.7
- `virtualenv`_.
- A working and configured `unison`_ installation, preferably
  installed with `homebrew`_.


Installation
============

::

    $ git clone https://github.com/jone/unison-tray.git
    $ cd unison-tray
    $ virtualenv . --setuptools
    $ source bin/activate
    $ pip install -r requirements.txt

``pip install`` will install PyObjC_, which may take awhile.


The path to unison is expected to be ``/usr/local/bin/unison``, change it in
the ``syncer.cfg`` if you have installed unison in another path.


Usage
=====

Be sure your unison configuration (``~/.unison/default.prf``) is configured so
that it works with only executing ``$ unison`` without root arguments.

You should create the initial copy before starting unison-tray, since unison
asks questions.

Start the tray icon from within the ``unison-tray`` directory with::

    $ bin/utray

From the menubar icon, "Sync now" will sync in the background, whereas "Resolve conflicts" will sync in a Terminal window.
All errors and messages are logged to ``var/utray.log`` in the unison-tray directory.


Autostart
=========

Add the ``utray.app`` to your autostart apps in the Mac OS user configuration.


License
=======

"THE BEER-WARE LICENSE" (Revision 42):

jone_ wrote this script. As long as you retain this notice you
can do whatever you want with this stuff. If we meet some day, and you think
this stuff is worth it, you can buy me a beer in return.


.. _unison: http://www.cis.upenn.edu/~bcpierce/unison
.. _homebrew: http://mxcl.github.com/homebrew/
.. _jone: http://github.com/jone
.. _PyObjC: https://pythonhosted.org/pyobjc/
.. _virtualenv: http://www.virtualenv.org
