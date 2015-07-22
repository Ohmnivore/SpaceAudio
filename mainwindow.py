from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from library import *
from controls import *
from ui_main import Ui_MainWindow
import time

class MainWindow(QMainWindow):
    def __init__(self, db_p, db_t, db_a, db_alb):
        super().__init__(None)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.hook_menubar()
        self.hook_ui()
        self.controls = Controls(self)
        self.lib = None
        self.db_p = db_p
        self.db_t = db_t
        self.db_a = db_a
        self.db_alb = db_alb
        self.refresh_lists()

    def hook_menubar(self):
        self.ui.actionManage_Library.triggered.connect(self.show_library_manager)
        self.ui.actionRescan_Library.triggered.connect(self.scan)
        self.ui.actionRescan_Library_Full.triggered.connect(self.hard_scan)

    def show_library_manager(self):
        self.lib = Library(self.db_p, self.db_t, self.db_a, self.db_alb, self)
        self.lib.show()

    def scan(self):
        Scanner(self, self.db_p.get_paths(), self.db_t, self.db_a, self.db_alb)

    def hard_scan(self):
        self.db_t.clear()
        Scanner(self, self.db_p.get_paths(), self.db_t, self.db_a, self.db_alb)

    def refresh_lists(self):
        self.refresh_artists(self.db_a.get_artists())
        self.refresh_albums(self.db_alb.get_albums())
        self.refresh_tracks(self.db_t.get_tracks())

    def refresh_artists(self, arr):
        self.ui.ArtistList.clear()
        self.ui.ArtistList.addItem('All')
        for artist in arr:
            self.ui.ArtistList.addItem(QListWidgetItem(artist))

    def refresh_albums(self, arr):
        self.ui.AlbumList.clear()
        self.ui.AlbumList.addItem('All')
        for album in arr:
            w = QListWidgetItem(album[1])
            w.setData(32, album[2])
            self.ui.AlbumList.addItem(w)

    def refresh_tracks(self, arr):
        self.ui.TrackTable.setRowCount(len(arr))
        for row in range(len(arr)):
            track = arr[row]
            self.ui.TrackTable.setItem(row, 0, QTableWidgetItem(track[3]))
            self.ui.TrackTable.setItem(row, 1, QTableWidgetItem(track[4]))
            self.ui.TrackTable.setItem(row, 2, QTableWidgetItem(track[5]))
            m, s = divmod(track[6], 60)
            h, m = divmod(m, 60)
            minutes = "%d:%02d" % (m, s)
            self.ui.TrackTable.setItem(row, 3, QTableWidgetItem(minutes))
            self.ui.TrackTable.setItem(row, 4, QTableWidgetItem(str(track[7])))
            self.ui.TrackTable.setItem(row, 5, QTableWidgetItem(track[1]))
            self.ui.TrackTable.setItem(row, 6, QTableWidgetItem(track[0]))
            self.ui.TrackTable.setItem(row, 7, QTableWidgetItem(str(round(track[8] / 1000000, 1)) + ' MB'))


    def hook_ui(self):
        self.ui.ArtistList.itemClicked.connect(self.chose_artist)
        self.ui.AlbumList.itemClicked.connect(self.chose_album)

    def chose_artist(self, widget):
        selection = widget.text()
        if selection == 'All':
            self.refresh_albums(self.db_alb.get_albums())
            self.refresh_tracks(self.db_t.get_tracks())
        else:
            self.refresh_albums(self.db_alb.get_albums_of_artist(selection))
            self.refresh_tracks(self.db_t.get_tracks_of_artist(selection))

    def chose_album(self, widget):
        album = widget.text()
        artist = widget.data(32)
        if album == 'All':
            cur = self.ui.ArtistList.currentItem()
            if cur == None or cur.text() == 'All':
                # Show tracks for all artists
                self.refresh_tracks(self.db_t.get_tracks())
            else:
                # Show all tracks for current artist
                self.refresh_tracks(self.db_t.get_tracks_of_artist(cur.text()))
        else:
            # Show tracks for current album
            self.refresh_tracks(self.db_t.get_tracks_of_artist_album(artist, album))
