import subprocess
import threading

class Play:
    def __init__(self, path, end_callback):
        self.path = path
        self.end_callback = end_callback
        self.thread = None
        self.proc = None
        self.was_killed = False
        # Launch thread
        self.thread = threading.Thread(target=self.play)
        self.thread.start()

    def play(self):
        self.proc = subprocess.Popen(["ffmpeg\\ffplay.exe", "-vn", "-nodisp", "-autoexit", "-hide_banner", "-nostats", "-loglevel", "quiet", "-i", self.path])
        self.proc.wait()
        if not self.was_killed:
            self.end_callback()

    def kill(self):
        if self.proc != None:
            self.was_killed = True
            self.proc.kill()
            self.proc = None
