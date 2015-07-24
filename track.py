class Track:
    def __init__(self):
        self.path = None
        self.fhash = None
        self.title = None
        self.artist = None
        self.album = None
        self.length = None
        self.track_number = None
        self.filename = None
        self.filesize = None

class DBTrackItem(Track):
    def __init__(self, arr):
        self.path = arr[0]
        self.filename = arr[1]
        self.fhash = arr[2]
        self.title = arr[3]
        self.artist = arr[4]
        self.album = arr[5]
        self.length = arr[6]
        self.track_number = arr[7]
        self.filesize = arr[8]
