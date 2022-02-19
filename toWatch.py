import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler


class Watcher:
    watch_dir = '.'

    def __init__(self):
        self.observer = Observer()

    def watch(self):
        event_handler = Handler()
        self.observer.schedule(event_handler, self.watch_dir, recursive=False)
        self.observer.start()
        try:
            while True:
                time.sleep(1)
        finally:
            self.observer.stop()
            self.observer.join()


class Handler(FileSystemEventHandler):
    def on_any_event(self, event):
        if event.is_directory:
            return None
        elif event.event_type == 'created':
            print('created')
        elif event.event_type == 'modified':
            print('modified')
