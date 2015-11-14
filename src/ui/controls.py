from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from ui.file_missing_dialog import *
from player.pyglet import *
import os
from util import util

class Controls:
    def __init__(self, mainwin):
        self.mainwin = mainwin
        self.table = self.mainwin.ui.TrackTable
        self.playlist = []
        self.curlist = []
        self.curplaying = 0
        self.player = Pyglet()
        self.last_item = None
        self.is_list = False

        self.loop = QTimer()
        self.loop.timeout.connect(self.update)
        self.loop.start(33)

        self.hook_ui()
        self.mainwin.ui.PlayPause.setIcon(QIcon('../assets/img/appbar.control.play.png'))

    def on_close(self):
        self.player.shutdown()

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
        self.curplaying = 0
        self.is_list = True
        for i in range(len(arr)):
            a = arr[i]
            if a.column() == 0:
                self.last_item = a
                self.add_item(a)
        if len(self.curlist) == 1:
            self.curlist = []
            self.is_list = False
            for i in range(self.table.rowCount()):
                self.add_item(self.table.item(i, 0))

    def add_item(self, item):
        self.curlist.append(item)


    def open_menu(self, position):
        menu = QMenu()
        act = QAction('Play', self.mainwin)
        act.triggered.connect(self.context_play)
        menu.addAction(act)
        menu.exec_(self.table.viewport().mapToGlobal(position))

    def context_play(self):
        if len(self.curlist) > 0:
            if self.is_list:
                self.curplaying = 0
            else:
                self.curplaying = self.last_item.row()
            self.playlist = self.curlist[:]
            self.color()
            self.play()

    def fix_slider(self):
        s = self.mainwin.ui.TrackSlider
        x = s.mapFromGlobal(QCursor.pos()).x()
        y = s.mapFromGlobal(QCursor.pos()).y()
        if len(self.playlist) > 0 and x >= 0 and y >= 0 and x <= s.width() and y <= s.height() and (QApplication.mouseButtons() & Qt.LeftButton):
            new_x = QStyle.sliderValueFromPosition(s.minimum(), s.maximum(), x, s.width())
            old_v = s.value()
            if old_v != new_x:
                track = self.playlist[self.curplaying].track
                s.setValue(new_x)
                self.player.seek(new_x / s.maximum() * track.length)

    def toggle_play(self):
        if self.player.timer.paused:
            self.mainwin.ui.PlayPause.setIcon(QIcon('../assets/img/appbar.control.pause.png'))
        else:
            self.mainwin.ui.PlayPause.setIcon(QIcon('../assets/img/appbar.control.play.png'))
        if len(self.playlist) > 0:
            self.player.toggle_play()

    def play(self):
        if len(self.playlist) > 0:
            track = self.playlist[self.curplaying].track
            if self.check_if_exists(track.path):
                self.mainwin.ui.PlayPause.setIcon(QIcon('../assets/img/appbar.control.pause.png'))
                self.color()
                self.player.timer.reset()
                self.mainwin.ui.TrackName.setText(track.title)
                self.mainwin.ui.TrackLength.setText(util.min_to_string(track.length))
                self.player.play(track, self.play_next, 0)
            else:
                dialog = FileMissingDialog(self.mainwin, track.path, self.remove_track, self.ignore_track)
                dialog.exec()
                self.stop()

    def remove_track(self):
        item = self.playlist[self.curplaying]
        self.mainwin.db_t.delete_track(item.track.path)
        self.table.removeRow(item.row())

    def ignore_track(self):
        pass

    def check_if_exists(self, path):
        return os.path.isfile(path) and os.access(path, os.R_OK)

    def color(self):
        for i in range(self.table.rowCount()):
            self.table.item(i, 0).setBackground(QBrush(QColor(45, 45, 45))) # dark grey
        for item in self.playlist:
            item.setBackground(QBrush(QColor(89, 145, 170))) # blue
        item = self.playlist[self.curplaying]
        item.setBackground(QBrush(QColor(117, 192, 149))) # green

    def stop(self):
        self.mainwin.ui.PlayPause.setIcon(QIcon('../assets/img/appbar.control.play.png'))
        self.player.stop()

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
        # Run refresh from main thread to avoid threading issues
        if self.mainwin.do_refresh:
            self.mainwin.refresh_lists(self.mainwin.db_t, self.mainwin.db_a, self.mainwin.db_alb)
            self.mainwin.do_refresh = False
        # Elapsed label
        if len(self.playlist) > 0:
            self.mainwin.ui.ElapsedTime.setText(util.min_to_string(self.player.timer.elapsed))
        # Volume code
        volume = self.mainwin.ui.VolumeSlider.value() / 100.0
        if len(self.playlist) > 0 and self.player.volume != volume:
            self.player.set_volume(volume)
        # Animate track progress slider
        if len(self.playlist) > 0:
            track = self.playlist[self.curplaying].track
            self.mainwin.ui.TrackSlider.setValue(float(self.player.timer.elapsed) * float(self.mainwin.ui.TrackSlider.maximum()) / float(track.length))
        # Update player
        self.player.update()
