import sqlite3
import pathlib


class Sqlite_handler:

    def __init__(self, path):

        self.path = path
        self.setup_db()
        
    def setup_db(self):
        self.path = pathlib.Path(self.path)
        self.con = sqlite3.connect(self.path)
        self.cur = self.con.cursor()

    def add_table(self, name, fields):
        if not isinstance(fields,tuple):
            fields = tuple(fields)
        self.cur.execute(f"CREATE TABLE IF NOT EXISTS {name}{fields}")
        self.con.commit()
        
    def list_tables(self):
        self.cur.execute("SELECT name FROM sqlite_master")
        tables = [tup[0] for tup in self.cur.fetchall()]
        print(tables)


    def add_row(self, table, data):
        values = ", ".join(data)
        self.cur.execute(f"INSERT INTO {table} VALUES {values}")
        self.con.commit()




handler = Sqlite_handler("./database.db")
handler.add_table("movie", ["title", "year", "score"])
handler.add_table("actors", ["age", "oscars", "IQ"])
handler.list_tables()
handler.add_row("movie", ["('Monty Python and the Holy Grail', 1975, 8.2)", "('And Now for Something Completely Different', 1971, 7.5)"])
handler.cur.execute("SELECT score FROM movie").fetchall()
