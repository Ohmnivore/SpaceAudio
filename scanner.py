import os, hashlib
import threading
from mutagen import File
from mutagen import mp3
from mutagen import flac
from mutagen import oggvorbis
from mutagen import mp4
from track import *
from info import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from popup import *
from db_track import *
from db_artist import *
from db_album import *

class Scanner:
    def __init__(self, mainwin, paths):
        self.mainwin = mainwin
        self.paths = paths

        self.info = Popup(self.mainwin)
        self.info.setWindowTitle('About')
        self.info.setWindowFlags(Qt.Dialog | Qt.FramelessWindowHint)
        self.info.ui.Text.setText('Scanning files... this may take a while.')
        self.info.ui.Ok.setEnabled(False)
        self.info.count = 0
        self.info.ui.Ok.setText('Files found: ' + str(self.info.count))
        self.info.show()

        self.scan()

    def scanfiles(self):
        db_t = DBTrack()
        db_a = DBArtist()
        db_alb = DBAlbum()
        for p in self.paths:
            self.scan_dir(p, db_t, db_a, db_alb)
        self.info.close()
        self.mainwin.do_refresh = True
        return

    def scan(self):
        t = threading.Thread(target=self.scanfiles)
        t.setDaemon(True)
        t.start()

    def scan_dir(self, path, db_t, db_a, db_alb):
        for dir_name, subdir_list, file_list in os.walk(path):
            for f in file_list:
                self.scan_file(os.path.join(dir_name, f), db_t, db_a, db_alb)
            for d in subdir_list:
                self.scan_dir(os.path.join(dir_name, d), db_t, db_a, db_alb)

    def scan_file(self, path, db_t, db_a, db_alb):
        base, ext = os.path.splitext(path)
        ext = ext.lower()
        if ext == '.mp3' or ext == '.flac' or ext == '.ogg' or ext == '.m4a':
            self.info.count += 1
            self.info.ui.Ok.setText('Files found: ' + str(self.info.count))
            FileData(path, db_t, db_a, db_alb)

class FileData(Track):
    def __init__(self, path, db_t, db_a, db_alb):
        super().__init__()
        self.path = path
        self.db_t = db_t
        self.db_a = db_a
        self.db_alb = db_alb
        self.is_recognized = False

        if not self.db_t.check_if_has(self.path):
            self.meta = File(path)
            self.filename = os.path.basename(self.path)
            #self.fhash = str(self.hash_file(self.path))
            self.fhash = ''
            self.filesize = int(os.path.getsize(self.path))
            try:
                if isinstance(self.meta, mp3.MP3):
                    self.is_recognized = True
                    self.title = self.meta.tags['TIT2'].text[0]
                    self.artist = self.meta.tags['TPE1'].text[0]
                    self.album = self.meta.tags['TALB'].text[0]
                    self.track_number = int(self.meta.tags['TRCK'].text[0].split('/')[0])
                elif isinstance(self.meta, flac.FLAC) or isinstance(self.meta, oggvorbis.OggVorbis):
                    self.is_recognized = True
                    self.title = self.meta.tags['TITLE'][0]
                    self.artist = self.meta.tags['Artist'][0]
                    self.album = self.meta.tags['Album'][0]
                    self.track_number = int(self.meta.tags['TRACKNUMBER'][0].split('/')[0])
                elif isinstance(self.meta, mp4.MP4):
                    self.is_recognized = True
                    self.title = self.meta.tags['©nam'][0]
                    self.artist = self.meta.tags['©ART'][0]
                    self.album = self.meta.tags['©alb'][0]
                    self.track_number = int(self.meta.tags['trkn'][0][0])
            except:
                pass

            if self.is_recognized:
                self.length = int(self.meta.info.length)
                if self.title == None:
                    self.title = self.filename
                if self.artist == None:
                    self.artist = 'Unknown'
                if self.album == None:
                    self.album = 'Unknown'
                if self.track_number == None:
                    self.track_number = 0

                self.db_t.insert_file(self)
                if not self.db_a.check_if_has(self.artist):
                    self.db_a.insert_name(self.artist)
                if not self.db_alb.check_if_has(self.artist + self.album):
                    self.db_alb.insert_album(self.artist + self.album, self.album, self.artist)

    def hash_file(self, path):
        BLOCKSIZE = 65536
        hasher = hashlib.sha1()
        with open(path, 'rb') as afile:
            buf = afile.read(BLOCKSIZE)
            while len(buf) > 0:
                hasher.update(buf)
                buf = afile.read(BLOCKSIZE)
        return hasher.hexdigest()
