from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from library import *
from popup import *
from controls import *
from track import *
from ui_main import Ui_MainWindow
import time
import util

class MainWindow(QMainWindow):
    def __init__(self, db_p, db_t, db_a, db_alb):
        super().__init__(None)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.hook_menubar()
        self.hook_ui()
        self.controls = Controls(self)
        self.lib = None
        self.track_map = {}
        self.db_p = db_p
        self.db_t = db_t
        self.db_a = db_a
        self.db_alb = db_alb
        self.refresh_lists()

        self.ui.TrackTable.setColumnWidth(0, 312)
        self.ui.TrackTable.setColumnWidth(1, 156)
        self.ui.TrackTable.setColumnWidth(2, 156)

    def closeEvent(self, event):
        self.controls.on_close()

    def hook_menubar(self):
        self.ui.actionManage_Library.triggered.connect(self.show_library_manager)
        self.ui.actionRescan_Library.triggered.connect(self.scan)
        self.ui.actionRescan_Library_Full.triggered.connect(self.hard_scan)
        self.ui.actionAbout.triggered.connect(self.show_about)
        self.ui.actionHelp.triggered.connect(self.show_help)
        self.ui.actionReport_Issue.triggered.connect(self.show_report)
        self.ui.actionContact.triggered.connect(self.show_contact)

    def show_about(self):
        about = Popup(self)
        about.setWindowTitle('About')
        about.ui.Text.setText(self.add_style_color(open('README.html', 'r').read()))
        about.show()
    def add_style_color(self, html):
        i = 0
        while i < len(html) - 1:
            if html[i] == '<' and html[i + 1] == 'a':
                html = html[:i + 2] +  ' style="color:#ecb447;"' + html[i + 2:]
            i += 1
        return html

    def show_help(self):
        about = Popup(self)
        about.setWindowTitle('Help')
        about.ui.Text.setText("""
            Check out our wiki: <a href="https://github.com/Ohmnivore/SpaceAudio/wiki" style="color:#ecb447;">https://github.com/Ohmnivore/SpaceAudio/wiki</a>
        """)
        about.show()

    def show_report(self):
        about = Popup(self)
        about.setWindowTitle('Report Issue')
        about.ui.Text.setText("""
            Please submit your issue to the GitHub tracker: <a href=https://github.com/Ohmnivore/SpaceAudio/issues style="color:#ecb447;">https://github.com/Ohmnivore/SpaceAudio/issues</a>
            <br/><br/>
            Do not hesitate, for every issue resolved brings us closer to world domination.
        """)
        about.show()

    def show_contact(self):
        about = Popup(self)
        about.setWindowTitle('Contact')
        about.ui.Text.setText("""
            Email: markbeiline@gmail.com <br/>
            Twitter: <a href="https://twitter.com/4_AM_Games" style="color:#ecb447;">@4_AM_Games</a> <br/>
            Website: <a href="http://fouramgames.com/" style="color:#ecb447;">http://fouramgames.com/</a>
        """)
        about.show()

    def show_library_manager(self):
        self.lib = Library(self.db_p, self.db_t, self.db_a, self.db_alb, self)
        self.lib.exec()

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
            w.setData(util.Roles.custom, album[2])
            self.ui.AlbumList.addItem(w)

    def refresh_tracks(self, arr):
        self.track_map = {}
        self.ui.TrackTable.setRowCount(len(arr))
        for row in range(len(arr)):
            track = DBTrackItem(arr[row], row)
            self.ui.TrackTable.setItem(row, 0, QTableWidgetItem(track.title))
            self.ui.TrackTable.setItem(row, 1, QTableWidgetItem(track.artist))
            self.ui.TrackTable.setItem(row, 2, QTableWidgetItem(track.album))
            if track.length != None:
                self.ui.TrackTable.setItem(row, 3, QTableWidgetItem(util.min_to_string(track.length)))
            self.ui.TrackTable.setItem(row, 4, QTableWidgetItem(str(track.track_number)))
            self.ui.TrackTable.setItem(row, 5, QTableWidgetItem(track.filename))
            self.ui.TrackTable.setItem(row, 6, QTableWidgetItem(track.path))
            self.ui.TrackTable.setItem(row, 7, QTableWidgetItem(util.filesize_to_string(track.filesize)))
            self.ui.TrackTable.item(row, 0).track = track;
        for r in range(self.ui.TrackTable.rowCount()):
            for c in range(self.ui.TrackTable.columnCount()):
                item = self.ui.TrackTable.item(r, c)
                if item != None:
                    item.setFlags(item.flags() & ~Qt.ItemIsEditable)


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
        artist = widget.data(util.Roles.custom)
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
