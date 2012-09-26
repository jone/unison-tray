from AppKit import NSApplication
from PyObjCTools import AppHelper
from utray.tray import TrayMenu
from utray.utils import create_icon
from utray.watcher import setup_observer


def run():
    app = NSApplication.sharedApplication()
    app.setActivationPolicy_(2)  # Hide from dock
    app.setApplicationIconImage_(create_icon('appicon.png'))

    traymenu = TrayMenu.alloc()
    traymenu.init()
    app.setDelegate_(traymenu)
    setup_observer(traymenu)
    AppHelper.runEventLoop()
