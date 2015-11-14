from PyQt5.QtCore import *
from PyQt5.QtGui import *
from ui.mainwindow import *
from ui.library import *
from db.db_path import *
from db.db_track import *
from db.db_artist import *
from db.db_album import *
from ui.process_style import *
from util.logger import *
import sys

import os.path
import traceback

def handle_exception(exc_type, exc_value, exc_traceback):
    """ handle all exceptions """
    ## KeyboardInterrupt is a special case.
    ## We don't raise the error dialog when it occurs.
    if issubclass(exc_type, KeyboardInterrupt):
        if qApp:
            qApp.quit()
        return
    sys.stderr.write(''.join(traceback.format_exception(exc_type, exc_value, exc_traceback)))
    sys.exit(1)

def open_r(path):
    return open(path, 'r').read()

def load_stylesheet(app, processor):
    style = open_r('../assets/style.css')
    style_list = open_r('../assets/style_list.css')
    style_table = open_r('../assets/style_table.css')
    app.setStyleSheet(processor.process(style) + processor.process(style_list) + processor.process(style_table))

if __name__ == '__main__':
    logger = Logger('SpaceAudio.log')
    sys.stdout = logger
    sys.stderr = logger
    sys.excepthook = handle_exception

    open('library.db', 'a').close()
    db_p = DBPath()
    db_t = DBTrack()
    db_a = DBArtist()
    db_alb = DBAlbum()

    app = QApplication(sys.argv)
    processor = StyleProcessor(open('../assets/vars.css', 'r').read())
    load_stylesheet(app, processor)
    w = MainWindow(db_p, db_t, db_a, db_alb)
    w.show()
    sys.exit(app.exec_())
