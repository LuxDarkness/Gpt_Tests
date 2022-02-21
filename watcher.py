import time
from watchdog.observers import Observer
from handler import Handler


class Watcher:
    def __init__(self, watch_dir='.'):
        self.watch_dir = watch_dir
        self.observer = Observer()

    def watch(self, log_path='.\\main_log.txt', proc_path='.\\Processed', not_path='.\\Not applicable',
              wb_path='.\\Master.xlsx'):
        event_handler = Handler(log_path, proc_path, not_path, wb_path)
        self.observer.schedule(event_handler, self.watch_dir, recursive=False)
        self.observer.start()
        try:
            while True:
                time.sleep(1)
        finally:
            self.observer.stop()
            self.observer.join()
