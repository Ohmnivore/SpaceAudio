import sqlite3 as sq

class DBAlbum:
    def __init__(self):
        self.con = None
        self.con = sq.connect('library.db')

        with self.con:
            cur = self.con.cursor()
            cur.execute(
            """
            CREATE TABLE IF NOT EXISTS albums
            (
                artistalbum TEXT PRIMARY KEY NOT NULL,
                name TEXT NOT NULL,
                artist TEXT NOT NULL
            )
            """)

    def check_if_has(self, artistalbum):
        with self.con:
            cur = self.con.cursor()
            cur.execute('SELECT EXISTS(SELECT 1 FROM albums WHERE artistalbum=? LIMIT 1)', (artistalbum,))
            return cur.fetchone()[0] == 1

    def insert_album(self, artistalbum, name, artist):
        with self.con:
            cur = self.con.cursor()
            cur.execute("""
                INSERT INTO albums (artistalbum, name, artist) VALUES (?, ?, ?)
            """, (artistalbum, name, artist,))
            self.con.commit()

    def get_albums(self):
        with self.con:
            cur = self.con.cursor()
            cur.execute('SELECT * FROM albums')
            return cur.fetchall()

    def get_albums_of_artist(self, artist):
        with self.con:
            cur = self.con.cursor()
            cur.execute('SELECT * FROM albums WHERE artist=?', (artist,))
            return cur.fetchall()
