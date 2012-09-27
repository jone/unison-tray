from AppKit import NSImage
import os


icons_dir = os.path.join(os.path.dirname(__file__), 'icons')


class AppRegistry(object):

    def __init__(self):
        self._app = None

    def get(self):
        if self._app is None:
            raise RuntimeError('No app registered yet.')
        return self._app

    def set(self, app):
        if self._app is not None:
            raise RuntimeError('App already registered.')
        self._app = app

app = AppRegistry()


def create_icon(name):
    path = os.path.join(icons_dir, name)
    return NSImage.alloc().initByReferencingFile_(path)


def get_root_path():
    confpath = os.path.expanduser('~/.unison/default.prf')

    config = open(confpath).readlines()
    roots = [line for line in config if line.startswith('root')]

    for line in roots:
        _, path = line.split('=', 1)
        path = path.strip()
        if '://' not in path:
            return os.path.abspath(path)

    raise Exception('Could not find root path in %s' % confpath)
