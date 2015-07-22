import sqlite3 as sq

class DBPath:
    def __init__(self):
        self.con = None
        self.con = sq.connect('library.db')

        with self.con:
            cur = self.con.cursor()
            cur.execute(
            """
            CREATE TABLE IF NOT EXISTS paths
            (
                path TEXT PRIMARY KEY NOT NULL
            )
            """)

    def get_paths(self):
        with self.con:
            cur = self.con.cursor()
            cur.execute('SELECT * FROM paths')

            arr = []
            for c in cur.fetchall():
                arr.append(c[0])
            return arr

    def set_paths(self, paths):
        with self.con:
            cur = self.con.cursor()
            cur.execute('DELETE FROM paths')
            for p in paths:
                cur.execute('INSERT INTO paths (path) VALUES (?)', (p,))
            self.con.commit()
