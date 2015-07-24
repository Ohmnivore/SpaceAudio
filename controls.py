from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from play import *
import time
import util

class Controls:
    def __init__(self, mainwin):
        self.mainwin = mainwin
        self.table = self.mainwin.ui.TrackTable
        self.playlist = []
        self.curlist = []
        self.curplaying = 0
        self.curproc = None

        self.start = None
        self.loop = QTimer()
        self.loop.timeout.connect(self.update_elapsed)
        self.loop.start(1000)

        self.hook_ui()

    def on_close(self):
        self.stop()

    def hook_ui(self):
        self.table.itemSelectionChanged.connect(self.chose_tracks)
        self.table.setContextMenuPolicy(Qt.CustomContextMenu)
        self.table.customContextMenuRequested.connect(self.open_menu)
        self.mainwin.ui.PreviousTrack.pressed.connect(self.previous_track)
        self.mainwin.ui.NextTrack.pressed.connect(self.next_track)

    def chose_tracks(self):
        self.curlist = []
        arr = self.table.selectedItems()
        last_row = 0
        self.curplaying = 0
        for i in range(len(arr)):
            a = arr[i]
            if a.column() == 0:
                last_row = a.row()
                self.add_row(last_row)
        if len(self.curlist) == 1:
            self.curlist = []
            self.curplaying = last_row
            for i in range(self.table.rowCount()):
                self.add_row(i)

    def add_row(self, row):
        track = self.mainwin.track_map[row]
        self.curlist.append(track)


    def open_menu(self, position):
        menu = QMenu()
        act = QAction('Play', self.mainwin)
        act.triggered.connect(self.context_play)
        menu.addAction(act)
        menu.exec_(self.table.viewport().mapToGlobal(position))

    def context_play(self):
        self.playlist = self.curlist[:]
        self.play()

    def play(self):
        self.stop()
        self.start = time.time()
        self.mainwin.ui.TrackName.setText(self.playlist[self.curplaying].title)
        self.mainwin.ui.TrackLength.setText(util.min_to_string(self.playlist[self.curplaying].length))
        self.curproc = Play(self.playlist[self.curplaying].path, self.play_next)

    def stop(self):
        if self.curproc != None:
            self.start = None
            self.curproc.kill()
            self.curproc = None

    def play_next(self):
        self.curplaying += 1
        if self.curplaying < len(self.playlist):
            self.play()

    def previous_track(self):
        self.curplaying -= 1
        if self.curplaying < 0:
            self.curplaying = 0
        self.stop()
        self.play()

    def next_track(self):
        self.curplaying += 1
        if self.curplaying >= len(self.playlist):
            self.curplaying = len(self.playlist) - 1
        self.stop()
        self.play()

    def update_elapsed(self):
        if self.start != None:
            end = time.time()
            diff = end - self.start
            self.mainwin.ui.ElapsedTime.setText(util.min_to_string(diff))
