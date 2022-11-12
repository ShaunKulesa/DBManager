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


    def add_rows(self, table, data):
        values = ", ".join(data)
        self.cur.execute(f"INSERT INTO {table} VALUES {values}")
        self.con.commit()

    def delete_row(self, table, pos):
        row_id = self.get_all_rows(table)[pos][1][0]
        self.cur.execute(f"DELETE FROM {table} WHERE rowid={row_id}")
        self.con.commit()

    def get_all_rows(self, table):

        self.cur.execute(f"SELECT rowid, * FROM {table};")
        return [i for i in enumerate(self.cur.fetchall())]

    def get_fields(self, table):
        self.cur.execute(f"PRAGMA table_xinfo({table})")
        return self.cur.fetchall()



handler = Sqlite_handler("./database.db")
#handler.add_table("movie", ["title", "year", "score"])
#handler.add_table("actors", ["age", "oscars", "IQ", "cache"])
handler.list_tables()
#handler.add_rows("movie", ["""("Monty Python and the Holy Grail", 1975, 8.2)""",
#                          """("And Now for Something Completely Different", 1971, 7.5)""",
#                          """("Monty Python Live at the Hollywood Bowl", 1982, 7.9)""",
#                          """("Monty Python's The Meaning of Life", 1983, 7.5)""",
#                          """("Monty Python's Life of Brian", 1979, 8.0)"""])
#handler.add_rows("actors", ["""("Tom Cruise", 2, -10, "2M")"""])
#handler.cur.execute("SELECT score FROM movie").fetchall()
for record in handler.get_all_rows('movie'):
    print(record)
#handler.delete_row("movie", 9)
