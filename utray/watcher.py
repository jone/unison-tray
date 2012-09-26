from utray.utils import get_root_path
from watchdog.events import FileSystemEventHandler
from watchdog.observers import Observer


class Handler(FileSystemEventHandler):

    def __init__(self, traymenu):
        self.traymenu = traymenu
        super(Handler, self).__init__()

    def on_any_event(self, event):
        paths = [event.src_path]
        if getattr(event, 'dest_path', None):
            paths.append(event.dest_path)

        print 'MODIFIED', paths


def setup_observer(traymenu):
    observer = Observer()
    observer.schedule(Handler(traymenu), path=get_root_path(), recursive=True)
    observer.start()
