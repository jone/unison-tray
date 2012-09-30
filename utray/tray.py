from AppKit import NSDate
from AppKit import NSDefaultRunLoopMode
from AppKit import NSMenu
from AppKit import NSMenuItem
from AppKit import NSObject
from AppKit import NSRunLoop
from AppKit import NSStatusBar
from AppKit import NSTimer
from AppKit import NSVariableStatusItemLength
from utray import interfaces
from utray.utils import create_icon
from utray.utils import app


start_time = NSDate.date()


ICONS =  {'inactive': create_icon('inactive.png'),
          'idle': create_icon('idle.png'),
          'syncing1': create_icon('active1.png'),
          'syncing2': create_icon('active2.png'),
          'syncing3': create_icon('active3.png'),
          'conflict': create_icon('error.png')}

STATUS_ICON_MAP = {
    interfaces.STATUS_INACTIVE: 'inactive',
    interfaces.STATUS_DISABLED: 'inactive',
    interfaces.STATUS_SYNCING: 'syncing',
    interfaces.STATUS_OK: 'idle',
    interfaces.STATUS_CONFLICT: 'conflict'}


class TrayMenu(NSObject):

    def applicationDidFinishLaunching_(self, notification):
        self._menu_items = {}

        self.statusbar = NSStatusBar.systemStatusBar()
        self._create_statusitem()
        self._create_menu()
        self._create_timer()

        self._syncing_icon_timer = None
        self._last_icon = None

        # sync on boot
        self.change_icon('inactive')
        app.get().sync(now=True)

    def _create_statusitem(self):
        self.trayicon = self.statusbar.statusItemWithLength_(
            NSVariableStatusItemLength)
        self.trayicon.setHighlightMode_(1)

    def _create_menu(self):
        self.menu = NSMenu.alloc().init()
        self.menu.setAutoenablesItems_(False)
        self.trayicon.setMenu_(self.menu)

        menuitem = NSMenuItem.alloc().initWithTitle_action_keyEquivalent_(
            'Status: loading', '', '')
        menuitem.setEnabled_(False)
        self._menu_items['status'] = menuitem
        self.menu.addItem_(menuitem)

        menuitem = NSMenuItem.alloc().initWithTitle_action_keyEquivalent_(
            'Sync now', 'sync:', '')
        menuitem.setEnabled_(False)
        self._menu_items['sync'] = menuitem
        self.menu.addItem_(menuitem)

        menuitem = NSMenuItem.alloc().initWithTitle_action_keyEquivalent_(
            'Resolve conflicts', 'resolve:', '')
        menuitem.setEnabled_(False)
        self._menu_items['resolve'] = menuitem
        self.menu.addItem_(menuitem)

        menuitem = NSMenuItem.alloc().initWithTitle_action_keyEquivalent_(
            app.get().status == interfaces.STATUS_DISABLED and 'Enable' or 'Disable',
            'enabledisable:', '')
        self._menu_items['enable_disable'] = menuitem
        self.menu.addItem_(menuitem)

        menuitem = NSMenuItem.alloc().initWithTitle_action_keyEquivalent_(
            'Quit', 'terminate:', '')
        self._menu_items['quit'] = menuitem
        self.menu.addItem_(menuitem)

    def _create_timer(self):
        timer = NSTimer.alloc() \
            .initWithFireDate_interval_target_selector_userInfo_repeats_(
            start_time, 1, self, 'tick:', None, True)
        NSRunLoop.currentRunLoop().addTimer_forMode_(timer, NSDefaultRunLoopMode)
        timer.fire()

    def status_changed(self, status):
        self._menu_items['status'].setTitle_('Status: %s' % status)

        self.change_icon(STATUS_ICON_MAP[status])

        if status == interfaces.STATUS_SYNCING:
            self._menu_items['sync'].setEnabled_(False)
            self._menu_items['resolve'].setEnabled_(False)
        elif status == interfaces.STATUS_DISABLED:
            self._menu_items['sync'].setEnabled_(False)
            self._menu_items['resolve'].setEnabled_(False)
        else:
            self._menu_items['sync'].setEnabled_(True)
            self._menu_items['resolve'].setEnabled_(True)

        if status == interfaces.STATUS_DISABLED:
            self._menu_items['enable_disable'].setTitle_('Enable')
        else:
            self._menu_items['enable_disable'].setTitle_('Disable')

    def sync_(self, notification):
        app.get().sync(now=True)

    def resolve_(self, notification):
        app.get().sync(foreground=True)

    def enabledisable_(self, notification):
        if app.get().status == interfaces.STATUS_DISABLED:
            app.get().set_status(interfaces.STATUS_INACTIVE)
            app.get().sync(now=True)
        else:
            app.get().set_status(interfaces.STATUS_DISABLED)

    def terminate_(self, notification):
        app.get().quit()
        super(TrayMenu, self).terminate_()

    def tick_(self, notification):
        last_status = getattr(self, '_last_status', None)
        current_status = app.get().status
        if last_status != current_status:
            self.status_changed(current_status)
            self._last_status = current_status

    def change_icon(self, name):
        if name == 'syncing':
            if self._last_icon is not None and self._last_icon.startswith('syncing'):
                return

            self.change_icon('syncing1')

            self._syncing_icon_timer = NSTimer.alloc() \
                .initWithFireDate_interval_target_selector_userInfo_repeats_(
                start_time, 1.0, self, 'animateSyncingIcon:', None, True)
            NSRunLoop.currentRunLoop().addTimer_forMode_(
                self._syncing_icon_timer, NSDefaultRunLoopMode)
            self._syncing_icon_timer.fire()
            return

        self._last_icon = name
        self.trayicon.setImage_(ICONS[name])

    def animateSyncingIcon_(self, notification):
        if self._syncing_icon_timer is None:
            return

        if not self._last_icon.startswith('syncing'):
            self._syncing_icon_timer.invalidate()
            self._syncing_icon_timer = None
            return

        index = int(self._last_icon[-1])
        index += 1
        if index > 3:
            index = 1

        name = 'syncing%i' % index
        self.change_icon(name)
