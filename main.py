from PyQt5.QtCore import *
from mainwindow import *
from library import *
from db_path import *
from db_track import *
from db_artist import *
from db_album import *
import sys

if __name__ == '__main__':
    open('library.db', 'a').close()
    db_p = DBPath()
    db_t = DBTrack()
    db_a = DBArtist()
    db_alb = DBAlbum()

    app = QApplication(sys.argv)
    w = MainWindow(db_p, db_t, db_a, db_alb)
    #w = Library(db_p)
    w.show()
    sys.exit(app.exec_())
