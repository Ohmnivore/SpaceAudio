from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from play import *
import util
from timer import *

class Controls:
    def __init__(self, mainwin):
        self.mainwin = mainwin
        self.table = self.mainwin.ui.TrackTable
        self.playlist = []
        self.curlist = []
        self.curplaying = 0
        self.curproc = None
        self.volume = 1

        self.timer = Timer()
        self.loop = QTimer()
        self.loop.timeout.connect(self.update)
        self.loop.start(33)

        self.hook_ui()

    def on_close(self):
        self.stop()

    def hook_ui(self):
        self.table.itemSelectionChanged.connect(self.chose_tracks)
        self.table.setContextMenuPolicy(Qt.CustomContextMenu)
        self.table.customContextMenuRequested.connect(self.open_menu)
        self.mainwin.ui.PreviousTrack.pressed.connect(self.previous_track)
        self.mainwin.ui.NextTrack.pressed.connect(self.next_track)
        self.mainwin.ui.PlayPause.pressed.connect(self.toggle_play)
        self.mainwin.ui.TrackSlider.valueChanged.connect(self.fix_slider)

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

    def fix_slider(self):
        s = self.mainwin.ui.TrackSlider
        x = s.mapFromGlobal(QCursor.pos()).x()
        y = s.mapFromGlobal(QCursor.pos()).y()
        if x >= 0 and y >= 0 and x <= s.width() and y <= s.height() and (QApplication.mouseButtons() & Qt.LeftButton):
            new_x = QStyle.sliderValueFromPosition(s.minimum(), s.maximum(), x, s.width())
            old_v = s.value()
            if old_v != new_x:
                s.setValue(new_x)
                # self.delta += new_x - old_v
                self.timer.set(new_x / s.maximum() * self.playlist[self.curplaying].length)
                self.pre_play()
                self.curproc = Play(self.playlist[self.curplaying].path, self.play_next, self.timer.elapsed, self.volume)

    def toggle_play(self):
        if self.timer.paused:
            self.pre_play()
            self.curproc = Play(self.playlist[self.curplaying].path, self.play_next, self.timer.elapsed, self.volume)
            self.timer.paused = False
        else:
            self.stop()
            self.timer.paused = True

    def pre_play(self):
        self.stop()
        self.timer.paused = False
        self.mainwin.ui.TrackName.setText(self.playlist[self.curplaying].title)
        self.mainwin.ui.TrackLength.setText(util.min_to_string(self.playlist[self.curplaying].length))

    def play(self):
        self.pre_play()
        self.timer.reset()
        self.curproc = Play(self.playlist[self.curplaying].path, self.play_next, 0, self.volume)

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

    def update(self):
        # Elapsed label
        if len(self.playlist) > 0:
            self.mainwin.ui.ElapsedTime.setText(util.min_to_string(self.timer.elapsed))
        # Volume code
        volume = self.mainwin.ui.VolumeSlider.value() / 100.0
        if len(self.playlist) > 0 and self.volume != volume:
            self.volume = volume
            self.stop()
            self.mainwin.ui.TrackName.setText(self.playlist[self.curplaying].title)
            self.mainwin.ui.TrackLength.setText(util.min_to_string(self.playlist[self.curplaying].length))
            self.curproc = Play(self.playlist[self.curplaying].path, self.play_next, self.timer.elapsed, self.volume)
        # Animate track progress slider
        if len(self.playlist) > 0:
            self.mainwin.ui.TrackSlider.setValue(float(self.timer.elapsed) * float(self.mainwin.ui.TrackSlider.maximum()) / float(self.playlist[self.curplaying].length))
