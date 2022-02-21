import os.path
import tkinter as tk
from tkinter import filedialog
from watcher import Watcher

if __name__ == '__main__':
    root = tk.Tk()
    root.withdraw()

    watch_route = filedialog.askdirectory(title='Folder a monitorear')
    proc_route = filedialog.askdirectory(title='Folder donde colocar los excel procesados')
    not_route = filedialog.askdirectory(title='Folder donde colocar los archivos no aptos para ser procesados')

    log_route = filedialog.askopenfilename(title='Seleccione el archivo de texto a usar como log',
                                           filetypes=[('Text files', '.txt')])

    master_route = filedialog.askopenfilename(title='Seleccione el archivo de excel para usar como consolidado',
                                              filetypes=[('Excel files', '.xlsx .xls .xlsb .xlsm')])

    if not watch_route:
        watch_route = '..\\Watch_Folder'
        if not os.path.exists(watch_route):
            os.makedirs(watch_route)

    if not proc_route:
        proc_route = '..\\Watch_Folder\\Processed'
        if not os.path.exists(proc_route):
            os.makedirs(proc_route)

    if not not_route:
        not_route = '..\\Watch_Folder\\Not applicable'
        if not os.path.exists(not_route):
            os.makedirs(not_route)

    if not log_route:
        log_route = '..\\Watch_Folder\\main_log.txt'
        if not os.path.exists(log_route):
            open(log_route, 'w').close()

    if not master_route:
        master_route = '..\\Watch_Folder\\master.xlsx'
        if not os.path.exists(master_route):
            open(master_route, 'w').close()

    watcher = Watcher(watch_dir=watch_route)
    watcher.watch(log_path=log_route, proc_path=proc_route, not_path=not_route, wb_path=master_route)
