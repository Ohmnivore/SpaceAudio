import os, hashlib
from mutagen import File

class Scanner:
    def __init__(self, mainwin, paths, db_t, db_a, db_alb):
        self.mainwin = mainwin
        self.paths = paths
        self.db_t = db_t
        self.db_a = db_a
        self.db_alb = db_alb
        for p in paths:
            self.scan_dir(p)
        self.mainwin.refresh_lists()

    def scan_dir(self, path):
        for dir_name, subdir_list, file_list in os.walk(path):
            for f in file_list:
                self.scan_file(os.path.join(dir_name, f))
            for d in subdir_list:
                self.scan_dir(os.path.join(dir_name, d))

    def scan_file(self, path):
        base, ext = os.path.splitext(path)
        if ext == '.mp3':
            FileData(path, self.db_t, self.db_a, self.db_alb)

class FileData:
    def __init__(self, path, db_t, db_a, db_alb):
        self.db_t = db_t
        self.db_a = db_a
        self.db_alb = db_alb
        self.path = path

        self.fhash = None
        self.title = None
        self.artist = None
        self.album = None
        self.length = None
        self.track_number = None
        self.filename = os.path.basename(self.path)
        self.filesize = None

        if not self.db_t.check_if_has(self.path):
            self.meta = File(path)
            self.fhash = str(self.hash_file(self.path))
            self.title = self.meta.tags['TIT2'].text[0]
            self.artist = self.meta.tags['TPE1'].text[0]
            self.album = self.meta.tags['TALB'].text[0]
            self.length = int(self.meta.info.length)
            self.track_number = int(self.meta.tags['TRCK'].text[0].split('/')[0])
            self.filesize = int(os.path.getsize(self.path))
            # print(self.fhash)
            # print(self.title)
            # print(self.artist)
            # print(self.album)
            # print(self.length)
            # print(self.track_number)
            # print(self.filesize)
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
