from toWatch import Watcher

watch_route = r'C:\Users\brand\Documents\Genpact\Progamming'
proc_route = r'C:\Users\brand\Documents\Genpact\Progamming\Processed'
not_route = r'C:\Users\brand\Documents\Genpact\Progamming\Not applicable'


if __name__ == '__main__':
    watcher = Watcher()
    watcher.watch()
