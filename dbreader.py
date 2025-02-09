import sqlite3


# класс чтения/записи бд
class DBreader:

    def __init__(self):
        self.con = sqlite3.connect('data/database.db')  # подключаемся
        self.id = 1  # айди игрока

    # получаем лучшие резы по уровням
    def get_best(self, level):
        best = self.con.cursor().execute(f"""SELECT {level}_best from player WHERE id = {self.id} """).fetchone()
        return best[0]

    # проверяем резы по уровням
    def check_best(self, time, level):
        best = self.con.cursor().execute(f"""SELECT {level}_best from player WHERE id = {self.id} """).fetchone()
        print(best)
        if best[0] > time:
            self.con.cursor().execute(f"""UPDATE player
                                        SET {level}_best = {time}
                                        WHERE id = {self.id} """).fetchall()
            self.con.commit()

    # получаем карты уровней
    def get_black_map(self):
        best = self.con.cursor().execute(f'''SELECT level_map from maps WHERE type = "black" ''').fetchone()
        return best[0]

    def get_red_map(self):
        best = self.con.cursor().execute(f'''SELECT level_map from maps WHERE type = "red" ''').fetchone()
        return best[0]

    def get_green_map(self):
        best = self.con.cursor().execute(f'''SELECT level_map from maps WHERE type = "green" ''').fetchone()
        return best[0]
