from util.timer import *

class Player:
    def __init__(self):
        self.timer = Timer()
        self.volume = 1
        self.track = None
        self.end_callback = None

    def update(self):
        pass

    def play(self, track, end_callback, seek = 0):
        self.timer.paused = False
        self.timer.set(seek)

    def stop(self):
        self.timer.paused = True

    def toggle_play(self):
        if self.timer.paused:
            self.play(self.track, self.end_callback, self.timer.elapsed)
        else:
            self.stop()

    def seek(self, elapsed):
        self.timer.set(elapsed)

    def set_volume(self, volume):
        self.volume = volume

    def shutdown(self):
        self.stop()
