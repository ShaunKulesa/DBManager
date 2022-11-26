import sqlite3
import pathlib


class SqliteHandler:

    def __init__(self, path):
        self.path = path
        
    def __enter__(self):
        self.path = pathlib.Path(self.path)
        self.con = sqlite3.connect(self.path)
        self.cur = self.con.cursor()
        return self
    
    def __exit__(self, exc_type, exc_value, traceback):
        self.con.close()

    def add_table(self, name, fields):
        if not isinstance(fields,tuple):
            fields = tuple(fields)
        self.cur.execute(f"CREATE TABLE IF NOT EXISTS {name}{fields}")
        self.con.commit()
        
    def list_tables(self):
        self.cur.execute("SELECT name FROM sqlite_master")
        tables = [tup[0] for tup in self.cur.fetchall()]
        print(tables)


    def add_records(self, table, data):
        table = ''.join( chr for chr in table if chr.isalnum() )
        values = ", ".join(data)
        self.cur.execute(f"INSERT INTO {table} VALUES {values}")
        self.con.commit()

    def get_all_records(self, table):
        table = ''.join( chr for chr in table if chr.isalnum() )
        self.cur.execute(f"SELECT rowid, * FROM {table} ;")
        return [i for i in enumerate(self.cur.fetchall())]

    def delete_record(self, table, pos):
        row_id = self.get_all_records(table)[pos][1][0]
        table = ''.join( chr for chr in table if chr.isalnum() )
        self.cur.execute(f"DELETE FROM {table} WHERE rowid={row_id}")
        self.con.commit()

    def get_record(self, table, pos):
        return self.get_all_records(table)[pos]    

    def get_fields(self, table):
        table = ''.join( chr for chr in table if chr.isalnum() )
        self.cur.execute(f"PRAGMA table_xinfo({table})")
        return [(i[0], i[1]) for i in self.cur.fetchall()]

    def edit_record(self, table, pos, data):
        table = ''.join( chr for chr in table if chr.isalnum() )
        fields = self.get_fields(table)
        row_id = self.get_all_records(table)[pos][1][0]
        if len(data) != len(fields):
            raise ValueError("incorrect number of fields")
        update = ", ".join([f"{field[1].upper()}={newval}" for field, newval in zip(fields, data) if newval!=None])
        print(f"""UPDATE '{table}' SET {update} WHERE rowid={row_id}""")
        self.cur.execute(f"""UPDATE '{table}' SET {update} WHERE rowid={row_id}""")
        self.con.commit()
        return True


# with SqliteHandler("./database.db") as sql:

    #sql.add_table("movie", ["title", "year", "score"])
    #sql.add_table("actors", ["age", "oscars", "IQ", "cache"])
    #sql.list_tables()
    #sql.add_records("movie", ["""("Monty Python and the Holy Grail", 1975, 8.2)""",
    #                          """("And Now for Something Completely Different", 1971, 7.5)""",
    #                          """("Monty Python Live at the Hollywood Bowl", 1982, 7.9)""",
    #                          """("Monty Python's The Meaning of Life", 1983, 7.5)""",
    #                          """("Monty Python's Life of Brian", 1979, 8.0)"""])
    #sql.add_records("actors", ["""("Tom Cruise", 2, -10, "2M")"""])
    #sql.cur.execute("SELECT score FROM movie").fetchall()
    #for record in sql.get_all_records('movie'):
    #    print(record)
    #sql.delete_row("movie", 0)
    #print(sql.get_fields('movie'))
    #print(sql.get_record('movie', 10))
    #print(sql.edit_record('movie', 10, ("'edited title'", None, 0)))
    #sql.delete_record('movie', 10)
    #print(sql.get_record('movie', 10))
