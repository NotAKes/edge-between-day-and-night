import sqlite3


class DBreader:
    def __init__(self):
        pass

    def get_track(self):
        con = sqlite3.connect('data/database.db')
        self.sound = con.cursor().execute(f""" pass """).fetchone()
        pass

