from utray.utils import app
from utray.utils import get_root_path
from watchdog.events import FileSystemEventHandler
from watchdog.observers import Observer


class Handler(FileSystemEventHandler):

    def __init__(self, app):
        self.app = app
        super(Handler, self).__init__()

    def on_any_event(self, event):
        paths = [event.src_path]
        if getattr(event, 'dest_path', None):
            paths.append(event.dest_path)

        app.get().sync()


def setup_observer(app):
    observer = Observer()
    observer.schedule(Handler(app), path=get_root_path(), recursive=True)
    observer.start()
    return observer
