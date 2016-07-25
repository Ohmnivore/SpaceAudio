import pyglet
from player.player import *

class Pyglet(Player):
    def __init__(self):
        Player.__init__(self)
        self.player = None

    def update(self):
        super().update()
        if self.track is not None and self.timer.elapsed >= self.track.length and self.end_callback is not None:
            self.end_callback()

    def play(self, track, end_callback, seek = 0):
        super().play(track, end_callback, seek)
        self.track = track
        self.end_callback = end_callback
        if self.player is not None:
            self.player.pause()
            self.player.delete()
        music = pyglet.media.load(track.path.encode('utf8'))
        self.player = music.play()
        self.player.seek(seek)
        self.timer.paused = False

    def stop(self):
        super().stop()
        if self.player is not None:
            self.player.pause()
        self.timer.paused = True

    def toggle_play(self):
        if self.player is None or self.track is None:
            return
        super().toggle_play()

    def seek(self, elapsed):
        super().seek(elapsed)
        if self.player is not None:
            self.player.seek(elapsed)

    def set_volume(self, volume):
        super().set_volume(volume)
        if self.player is not None:
            self.player.volume = self.volume

    def shutdown(self):
        super().shutdown()
        if self.player is not None:
            self.player.delete()
        pyglet.app.exit()
