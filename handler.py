import os.path
import logging
import pythoncom
import xlwings as xw
from watchdog.events import FileSystemEventHandler


class Handler(FileSystemEventHandler):
    formatter = logging.Formatter('%(asctime)s %(lineno)d %(levelname)s:%(message)s')
    ignore_strings = ['~$', '.py', '.gitignore']

    def __init__(self, log_path, proc_path, not_path, main_wb_path):
        self.log_path = log_path
        self.proc_path = proc_path
        self.not_path = not_path
        self.main_wb_path = main_wb_path
        self.ignore_strings.append(os.path.basename(main_wb_path))
        self.ignore_strings.append(os.path.basename(log_path))
        self.logger = self.create_logger()

    def create_logger(self):
        if not os.path.exists(self.log_path):
            open(self.log_path, 'w').close()

        log_handler = logging.FileHandler(self.log_path)
        log_handler.setFormatter(self.formatter)
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(self.formatter)

        logger = logging.getLogger('Main')
        logger.setLevel(logging.INFO)
        logger.addHandler(log_handler)
        logger.addHandler(console_handler)

        return logger

    def process_excel(self, file_path, move_to):
        self.logger.info('Archivo excel encontrado, procesandolo...')

        # noinspection PyUnresolvedReferences
        pythoncom.CoInitialize()

        with xw.App(visible=False):
            other_name = os.path.basename(file_path)
            main_wb = xw.Book(self.main_wb_path)
            other_wb = xw.Book(file_path)
            try:
                for sheet in range(1, other_wb.sheets.count + 1):
                    act_ws = other_wb.sheets(sheet)
                    act_ws.copy(before=main_wb.sheets[0], name=other_name + '_' + act_ws.name)
            except ValueError:
                self.logger.warning('{} ya ha sido procesado previamente, solamente se moverá.'.format(other_name))
            other_wb.close()
            main_wb.save()
            main_wb.app.quit()

        self.logger.info('Archivo procesado, moviéndolo a la carpeta de procesados.')
        self.move_file(file_path, move_to)

    def move_file(self, file, move_to):
        file_name = os.path.basename(file)
        try:
            os.rename(file, move_to + '\\' + file_name)
            self.logger.info('El archivo {} fue movido a la carpeta {} correctamente.'.format(file_name, move_to))
        except FileExistsError:
            self.logger.warning('El archivo {} ya existe en la carpeta {}, no es posible moverlo.'.format(
                file_name, move_to))

    def on_any_event(self, event):
        base_name = os.path.basename(event.src_path)
        if event.is_directory:
            return None
        elif any([pattern in base_name for pattern in self.ignore_strings]) or '.' not in base_name:
            print('Se ignoró el archivo: {} en el directorio observado.'.format(base_name))
            return None
        elif event.event_type == 'created':
            self.logger.info('Un nuevo archivo ha sido encontrado en la carpeta observada.')
            if event.src_path[-5:-1] == '.xls' or event.src_path[-4:] == '.xls':
                self.process_excel(event.src_path, self.proc_path)
            else:
                self.logger.info('El nuevo archivo no es aplicable para ser procesado, moviéndolo...')
                self.move_file(event.src_path, self.not_path)
        elif event.event_type == 'deleted' or event.event_type == 'modified':
            self.logger.info('A file has been {} in the observed directory'.format(event.event_type))
