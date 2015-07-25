from player import *
from timer import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from play import *

class Ffmpeg(Player):
    def __init__(self):
        self.curproc = None
        self.volume = 1
        self.track = None
        self.end_callback = None
        self.timer = Timer()

    def play(self, track, end_callback, seek = 0):
        self.track = track
        self.end_callback = end_callback
        self.stop()
        self.timer.paused = False
        # self.timer.reset()
        self.curproc = Play(self.track.path, self.end_callback, seek, self.volume)

    def stop(self):
        if self.curproc != None:
            self.curproc.kill()
            self.curproc = None
            self.timer.paused = True

    def toggle_play(self):
        if self.timer.paused:
            self.play(self.track, self.end_callback, self.timer.elapsed)
            self.timer.paused = False
        else:
            self.stop()
            self.timer.paused = True

    def seek(self, elapsed):
        self.timer.set(elapsed)
        if not self.timer.paused:
            self.play(self.track, self.end_callback, self.timer.elapsed)

    def set_volume(self, volume):
        self.volume = volume
        if not self.timer.paused:
            self.play(self.track, self.end_callback, self.timer.elapsed)
