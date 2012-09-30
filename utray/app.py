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



class Application(object):

    def __init__(self, path_to_unison):
        self.path_to_unison = path_to_unison
        app.set(self)

        if self._is_persistent_disabled():
            self._status = interfaces.STATUS_DISABLED
        else:
            self._status = interfaces.STATUS_INACTIVE

    def run(self):
        self._syncer = Syncer(self.path_to_unison)
        self._syncer.start()

        app = NSApplication.sharedApplication()
        app.setActivationPolicy_(2)  # Hide from dock
        app.setApplicationIconImage_(create_icon('appicon.png'))

        self.traymenu = TrayMenu.alloc()
        self.traymenu.init()
        app.setDelegate_(self.traymenu)

        setup_observer(self)
        setup_syncing_cronjobs()

        AppHelper.runEventLoop()

    @property
    def status(self):
        return self._status

    def set_status(self, status):
        if interfaces.STATUS_DISABLED in (status, self.status) and \
                not status == self.status:
            self._persist_disabled(status == interfaces.STATUS_DISABLED)

        self._status = status
        self.traymenu.status_changed(status)

    def sync(self, foreground=False, now=False):
        if self.status == interfaces.STATUS_DISABLED:
            return False

        else:
            self._syncer.sync(foreground=foreground, now=now)
            return True

    def quit(self):
        self._syncer.stop()

    def _persist_disabled(self, disabled):
        path = os.path.join(os.getcwd(), 'var', 'disabled')
        file_ = open(path, 'w+')
        file_.write(str(disabled))
        file_.close()

    def _is_persistent_disabled(self):
        path = os.path.join(os.getcwd(), 'var', 'disabled')
        if not os.path.isfile(path):
            return False

        data = open(path).read().strip().lower()
        return data == 'true'

def run(path_to_unison):
    Application(path_to_unison).run()
