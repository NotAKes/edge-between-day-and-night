import sqlite3


class DBreader:
    def __init__(self):
        self.sound = None
        self.con = sqlite3.connect('data/database.db')

    def get_track(self):
        self.sound = self.con.cursor().execute(f""" pass """).fetchone()

    def red_aviable(self):
        is_red_aviable = self.con.cursor().execute(f""" pass """).fetchone()
        return is_red_aviable

    def green_aviable(self):
        is_green_aviable = self.con.cursor().execute(f""" pass """).fetchone()
        return is_green_aviable

    def get_best(self):
        best = self.con.cursor().execute(f""" pass """).fetchone()
        return best

    def check_best(self, time):
        best = self.con.cursor().execute(f""" pass """).fetchone()

    def get_black_map(self):
        best = self.con.cursor().execute(f'''SELECT level_map from maps WHERE type = "black" ''').fetchone()
        return best[0]

    def get_red_map(self):
        best = self.con.cursor().execute(f'''SELECT level_map from maps WHERE type = "red" ''').fetchone()
        return best[0]

    def get_green_map(self):
        best = self.con.cursor().execute(f'''SELECT level_map from maps WHERE type = "green" ''').fetchone()
        return best[0]


db = DBreader()
print(db.get_black_map())
