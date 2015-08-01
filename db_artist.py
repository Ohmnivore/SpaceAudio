import sqlite3 as sq

class DBArtist:
    def __init__(self):
        self.con = None
        self.con = sq.connect('library.db')

        with self.con:
            cur = self.con.cursor()
            cur.execute(
            """
            CREATE TABLE IF NOT EXISTS artists
            (
                name TEXT PRIMARY KEY NOT NULL
            )
            """)

    def check_if_has(self, name):
        with self.con:
            cur = self.con.cursor()
            cur.execute('SELECT EXISTS(SELECT 1 FROM artists WHERE name=? LIMIT 1)', (name,))
            return cur.fetchone()[0] == 1

    def insert_name(self, name):
        with self.con:
            cur = self.con.cursor()
            cur.execute("""
                INSERT INTO artists (name) VALUES (?)
            """, (name,))
            self.con.commit()

    def get_artists(self):
        with self.con:
            cur = self.con.cursor()
            cur.execute('SELECT * FROM artists ORDER BY name ASC')

            arr = []
            for c in cur.fetchall():
                arr.append(c[0])
            return arr
