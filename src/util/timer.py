from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

class Timer:
    def __init__(self):
        self.elapsed = 0
        self.paused = False
        self.loop = QTimer()
        self.loop.timeout.connect(self.update)
        self.loop.start(1000)

    def update(self):
        if not self.paused:
            self.elapsed += 1

    def toggle(self):
        self.paused = not self.paused

    def pause(self):
        self.paused = True

    def resume(self):
        self.paused = False

    def reset(self):
        self.elapsed = 0

    def set(self, elapsed):
        self.elapsed = elapsed
