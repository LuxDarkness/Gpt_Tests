from watcher import Watcher

watch_route = r'C:\Users\brand\Documents\Genpact\Tests_Route'
proc_route = r'C:\Users\brand\Documents\Genpact\Tests_Route\Processed'
not_route = r'C:\Users\brand\Documents\Genpact\Tests_Route\Not applicable'


if __name__ == '__main__':
    watcher = Watcher(watch_route)
    watcher.watch(proc_path=proc_route, not_path=not_route)
