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


start_time = NSDate.date()


ICONS =  {'inactive': create_icon('inactive.png'),
          'idle': create_icon('idle.png'),
          'syncing1': create_icon('active1.png'),
          'syncing2': create_icon('active2.png'),
          'syncing3': create_icon('active3.png'),
          'conflict': create_icon('error.png')}

STATUS_ICON_MAP = {
    interfaces.STATUS_INACTIVE: 'inactive',
    interfaces.STATUS_SYNCING: 'syncing',
    interfaces.STATUS_OK: 'idle',
    interfaces.STATUS_CONFLICT: 'conflict'}


class TrayMenu(NSObject):

    def applicationDidFinishLaunching_(self, notification):
        self._menu_items = {}

        self._status = interfaces.STATUS_INACTIVE

        self.statusbar = NSStatusBar.systemStatusBar()
        self._create_statusitem()
        self._create_menu()
        self._create_timer()
        self.set_status(interfaces.STATUS_INACTIVE)

        self._syncing_icon_timer = None
        self._last_icon = None

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
        self._menu_items['sync'] = menuitem
        self.menu.addItem_(menuitem)

        menuitem = NSMenuItem.alloc().initWithTitle_action_keyEquivalent_(
            'Resolve conflicts', 'resolve:', '')
        menuitem.setEnabled_(False)
        self._menu_items['resolve'] = menuitem
        self.menu.addItem_(menuitem)

        menuitem = NSMenuItem.alloc().initWithTitle_action_keyEquivalent_(
            'Quit', 'terminate:', '')
        self._menu_items['quit'] = menuitem
        self.menu.addItem_(menuitem)

    def _create_timer(self):
        timer = NSTimer.alloc() \
            .initWithFireDate_interval_target_selector_userInfo_repeats_(
            start_time, 5.0, self, 'tick:', None, True)
        NSRunLoop.currentRunLoop().addTimer_forMode_(timer, NSDefaultRunLoopMode)
        timer.fire()

    def set_status(self, status):
        self._status = status
        self._menu_items['status'].setTitle_('Status: %s' % status)

        self.change_icon(STATUS_ICON_MAP[status])

    @property
    def status(self):
        self.status

    def sync_(self, notification):
        # XXX
        self._menu_items['sync'].setEnabled_(False)
        self.set_status(interfaces.STATUS_SYNCING)

    def resolve_(self, notification):
        pass

    def tick_(self, notification):
        pass  # idle

    def syncing(self, is_syncing):
        has_conflicts = False

        for action, context in self.action_context_map.items():
            action.setTitle_(context.get_menu_title())
            action.setEnabled_(not is_syncing)
            if not is_syncing and context.status == STATUS_CONFLICT:
                has_conflicts = True

        self._menu_items['sync'].setEnabled_(not is_syncing)

        if has_conflicts:
            self.change_icon('conflict')
        elif is_syncing:
            self.change_icon('syncing')
        else:
            self.change_icon('idle')

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
