from utray import interfaces
from utray.config import CONFIG
from utray.utils import app
import os
import threading
import time


DELAY_TIMEOUT = 5  # in seconds

NO_SYNC = 0
SYNC_DELAYED_BG = 1
SYNC_NOW_BG = 2
SYNC_NOW_FG = 3


terminal_cmd_template = """osascript -e \'
tell application "Terminal" to activate
tell application "Terminal" to do script "%s" in window 1\'
"""


class Syncer(threading.Thread):

    def __init__(self):
        super(Syncer, self).__init__()
        self._syncing = False
        self._running = True
        self._pending = NO_SYNC

    def sync(self, foreground=False, now=False):
        if foreground and self._syncing:
            raise RuntimeError(
                'Syncing in foreground is not possible when already syncing.')

        if foreground:
            self._pending = SYNC_NOW_FG

        elif now:
            self._pending = SYNC_NOW_BG

        else:
            self._pending = SYNC_DELAYED_BG

    def stop(self):
        self._running = False

    def run(self):
        interval = range(DELAY_TIMEOUT)
        try:
            while True:

                if self._pending is not NO_SYNC:
                    self._execute()

                for _i in interval:
                    if self._pending not in (SYNC_NOW_FG, SYNC_NOW_BG):
                        time.sleep(1)

        except KeyboardInterrupt:
            return

    def _execute(self):
        foreground = self._pending == SYNC_NOW_FG
        self._pending = NO_SYNC

        if app.get().status is interfaces.STATUS_SYNCING:
            print 'Syncer quit: already syncing'
            return

        elif app.get().status is interfaces.STATUS_DISABLED:
            print 'Syncer quit: app is disabled'
            return

        else:
            app.get().set_status(interfaces.STATUS_SYNCING)

        if foreground:
            cmd = terminal_cmd_template % '%s -auto' % (
                CONFIG.unison_executable)
        else:
            cmd = '%s -batch' % CONFIG.unison_executable

        try:
            self._finished(self._runcmd(cmd))
        except Exception, exc:
            # XXX improve error handling
            print str(exc)
            self._finished(False)
            raise exc

    def _finished(self, exitcode):
        if exitcode == 0:
            app.get().set_status(interfaces.STATUS_OK)
        else:
            app.get().set_status(interfaces.STATUS_CONFLICT)

    def _runcmd(self, cmd):
        return os.system(cmd)
