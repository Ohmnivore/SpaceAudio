import subprocess
import threading

class Play:
    def __init__(self, path, end_callback, seek = 0, volume = 1):
        self.path = path
        self.end_callback = end_callback
        self.seek = seek
        self.volume = volume
        self.thread = None
        self.proc = None
        self.was_killed = False
        # Launch thread
        self.thread = threading.Thread(target=self.play)
        self.thread.start()

    def play(self):
        self.proc = subprocess.Popen(["ffmpeg\\ffplay.exe", "-vn", "-nodisp", "-autoexit", "-hide_banner", "-nostats", "-loglevel", "quiet", "-ss", str(self.seek), "-af", 'volume=' + str(self.volume), "-i", self.path])
        self.proc.wait()
        if not self.was_killed:
            self.end_callback()

    def kill(self):
        if self.proc != None:
            self.was_killed = True
            self.proc.kill()
            self.proc = None
