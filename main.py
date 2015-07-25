from PyQt5.QtCore import *
from PyQt5.QtGui import *
from mainwindow import *
from library import *
from db_path import *
from db_track import *
from db_artist import *
from db_album import *
from process_style import *
import sys

def load_stylesheet(app, processor, path):
    sheet = open(path, 'r').read()
    app.setStyleSheet(processor.process(sheet))

if __name__ == '__main__':
    open('library.db', 'a').close()
    db_p = DBPath()
    db_t = DBTrack()
    db_a = DBArtist()
    db_alb = DBAlbum()

    app = QApplication(sys.argv)
    processor = StyleProcessor(open('vars.css', 'r').read())
    load_stylesheet(app, processor, 'style.css')
    w = MainWindow(db_p, db_t, db_a, db_alb)
    w.show()
    sys.exit(app.exec_())
