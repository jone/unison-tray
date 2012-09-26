from AppKit import NSImage
import os


icons_dir = os.path.join(os.path.dirname(__file__), 'icons')


def create_icon(name):
    path = os.path.join(icons_dir, name)
    return NSImage.alloc().initByReferencingFile_(path)


def get_root_path():
    confpath = os.path.expanduser('~/.unison/default.prf')

    config = open(confpath).readlines()
    roots = [line for line in config if line.startswith('root')]

    for line in roots:
        _, path = line.split('=', 1)
        print (_, path)
        path = path.strip()
        if '://' not in path:
            return os.path.abspath(path)

    raise Exception('Could not find root path in %s' % confpath)
