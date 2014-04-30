from AppKit import NSApplication
from PyObjCTools import AppHelper
from utray import interfaces
from utray.cron import setup_syncing_cronjobs
from utray.syncer import Syncer
from utray.tray import TrayMenu
from utray.utils import app
from utray.utils import create_icon
from utray.watcher import setup_observer
import os.path
import signal


def sigint_handler(signum, frame):
    app.get().quit()
    signal.signal(signal.SIGINT, signal.default_int_handler)


DISABLING_STATE_FILE_PATH = os.path.abspath(os.path.join(
        os.path.dirname(__file__), '..', 'var', 'disabled'))


class Application(object):

    def __init__(self):
        app.set(self)

        if self._is_persistent_disabled():
            self._status = interfaces.STATUS_DISABLED
        else:
            self._status = interfaces.STATUS_INACTIVE

    def run(self):
        self._syncer = Syncer()
        self._syncer.start()

        app = NSApplication.sharedApplication()
        app.setActivationPolicy_(2)  # Hide from dock
        app.setApplicationIconImage_(create_icon('appicon.png'))

        self.traymenu = TrayMenu.alloc()
        self.traymenu.init()
        app.setDelegate_(self.traymenu)

        self._observer = setup_observer(self)
        self._cron = setup_syncing_cronjobs()

        AppHelper.runEventLoop()

    @property
    def status(self):
        return self._status

    def set_status(self, status):
        if interfaces.STATUS_DISABLED in (status, self.status) and \
                not status == self.status:
            self._persist_disabled(status == interfaces.STATUS_DISABLED)

        self._status = status

    def sync(self, foreground=False, now=False):
        if self.status == interfaces.STATUS_DISABLED:
            return False

        else:
            self._syncer.sync(foreground=foreground, now=now)
            return True

    def quit(self):
        AppHelper.stopEventLoop()
        self._syncer.stop()
        self._observer.stop()
        for thread in self._cron:
            thread.stop()

    def _persist_disabled(self, disabled):
        file_ = open(DISABLING_STATE_FILE_PATH, 'w+')
        file_.write(str(disabled))
        file_.close()

    def _is_persistent_disabled(self):
        if not os.path.isfile(DISABLING_STATE_FILE_PATH):
            return False

        data = open(DISABLING_STATE_FILE_PATH).read().strip().lower()
        return data == 'true'

def run():
    signal.signal(signal.SIGINT, sigint_handler)
    Application().run()
