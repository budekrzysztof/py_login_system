import sqlite3

class DatabaseConnection:
    def __enter__(self):
        self.con = sqlite3.connect('database/database.db')
        return self.con

    def __exit__(self, *args):
        self.con.close()