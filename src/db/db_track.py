import sqlite3 as sq

class DBTrack:
    def __init__(self):
        self.con = None
        self.con = sq.connect('library.db')

        with self.con:
            cur = self.con.cursor()
            cur.execute(
            """
            CREATE TABLE IF NOT EXISTS tracks
            (
                path TEXT PRIMARY KEY NOT NULL,
                filename TEXT NOT NULL,
                fhash TEXT NOT NULL,
                title TEXT,
                artist TEXT,
                album TEXT,
                length INTEGER,
                track_number INTEGER,
                filesize INTEGER
            )
            """)

    def clear(self):
        with self.con:
            cur = self.con.cursor()
            cur.execute('DELETE FROM tracks')
            self.con.commit()

    def delete_track(self, path):
        with self.con:
            cur = self.con.cursor()
            cur.execute('DELETE FROM tracks WHERE path=?', (path,))
            self.con.commit()

    def check_if_has(self, path):
        with self.con:
            cur = self.con.cursor()
            cur.execute('SELECT EXISTS(SELECT 1 FROM tracks WHERE path=? LIMIT 1)', (path,))
            return cur.fetchone()[0] == 1

    def insert_file(self, f):
        with self.con:
            cur = self.con.cursor()
            cur.execute("""
                INSERT INTO tracks (path, filename, fhash, title, artist, album, length, track_number, filesize) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (f.path, f.filename, f.fhash, f.title, f.artist, f.album, f.length, f.track_number, f.filesize,))
            self.con.commit()

    def get_tracks(self):
        with self.con:
            cur = self.con.cursor()
            cur.execute('SELECT * FROM tracks ORDER BY album, track_number ASC')
            return cur.fetchall()

    def get_tracks_of_artist(self, artist):
        with self.con:
            cur = self.con.cursor()
            cur.execute('SELECT * FROM tracks WHERE artist=? ORDER BY album, track_number ASC', (artist,))
            return cur.fetchall()

    def get_tracks_of_album(self, album):
        with self.con:
            cur = self.con.cursor()
            cur.execute('SELECT * FROM tracks WHERE album=? ORDER BY album, track_number ASC', (album,))
            return cur.fetchall()

    # def get_tracks_of_artist_album(self, artist, album):
    #     with self.con:
    #         cur = self.con.cursor()
    #         cur.execute('SELECT * FROM tracks WHERE artist=? AND album=? ORDER BY album, artist, track_number ASC', (artist, album,))
    #         return cur.fetchall()
