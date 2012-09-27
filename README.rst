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
- Syncs on application start.
- It just calls ``unison -batch`` (background) or ``unison -auto`` (foreground for
  conflict resolution). It does not configure unison in any other way.

.. image:: https://github.com/jone/unison-tray/raw/master/screenshot.png



Compatibility
=============

- Mac OS X (Tested with 10.6 and 10.7).
- python 2.7 with cocoa bindings, as installed on every compatible Mac OS X.
- A working and configured `unison`_ installation, preferably
  installed with `homebrew`_.


Installation
============

::

    $ git clone https://github.com/jone/unison-tray.git
    $ cd unison-tray
    $ /usr/bin/python2.7 bootstrap.py
    $ bin/buildout

You may need to change the path to your unison installation in buildout.cfg (a bin/buildout rerun is required).


Usage
=====

Be sure your unison configuration (``~/.unison/default.prf``) is configured so
that it works with only executing ``$ unison`` without root arguments.

You should create the initial copy before starting unison-tray, since unison
asks questions.

Start the tray icon from within the ``unison-tray`` directory with:

    $ bin/utray


Autostart
=========

There are several ways to automatically start the application on login by
executing ``bin/utray``, documented in the
`world wide web <http://stackoverflow.com/questions/6442364/running-script-upon-login-mac>`_.

That's how you can make the application automatically start when you start your computer:

    $ cd /Library/StartupItems
    $ sudo mkdir utray
    $ cd utray
    $ sudo ln -s /PATH/TO/YOUR/INSTALLATION/bin/utray utray

(The directory and the symlink within the directory need to have the same name!)


License
=======

"THE BEER-WARE LICENSE" (Revision 42):

jone_ wrote this script. As long as you retain this notice you
can do whatever you want with this stuff. If we meet some day, and you think
this stuff is worth it, you can buy me a beer in return.


.. _unison: http://www.cis.upenn.edu/~bcpierce/unison
.. _homebrew: http://mxcl.github.com/homebrew/
.. _jone: http://github.com/jone
