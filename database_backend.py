import sqlite3
import pathlib


class SqliteHandler:

    def __init__(self, path):
        self.path = path
        
    def __enter__(self):
        
        self.path = pathlib.Path(self.path)
        self.con = sqlite3.connect(self.path)
        self.cur = self.con.cursor()

        #create a dictionary to convert database types to python types
        self.types = {
            "INTEGER": int,
            "TEXT": str,
            "REAL": float,
            "BLOB": bytes
        }
        # self.types
        return self
    
    def __exit__(self, exc_type, exc_value, traceback):
        self.con.close()

    # def begin(self):
    #     self.cur.execute("BEGIN")
    
    # def end(self):
    #     self.con.execute("END")

    def add_table(self, name, fields):
        if not isinstance(fields,tuple):
            fields = tuple(fields)
        self.cur.execute(f"CREATE TABLE IF NOT EXISTS {name} {fields}")
        # self.con.commit()
        
    def list_tables(self):
        self.cur.execute("SELECT name FROM sqlite_master WHERE type='table' AND name!='sqlite_stat1'")
        tables = [tup[0] for tup in self.cur.fetchall()]
        return tables

    def add_records(self, table, data):
        self.cur.execute(f"INSERT INTO {table} VALUES {data}")
        # self.con.commit()

    def get_all_records(self, table):
        self.cur.execute(f"SELECT * FROM {table} ;")
        return self.cur.fetchall()

    def delete_record(self, table, pos):
        row_id = self.get_all_records(table)[pos][0]
        table = ''.join( chr for chr in table if chr.isalnum())
        self.cur.execute(f"DELETE FROM {table} WHERE rowid={row_id}")
    
    def delete_records(self, table, selection):
        row_ids = [record[0] for record in self.get_all_records(table)[selection]]
        table = ''.join(chr for chr in table if chr.isalnum())
        # print("row"row_ids)
        self.cur.execute(f"DELETE FROM {table} WHERE rowid IN {tuple(row_ids)}")

    def get_record(self, table, pos):
        return self.get_all_records(table)[pos]    

    def get_fields(self, table):
        self.cur.execute(f"PRAGMA table_xinfo({table})")
        return [(i[1]) for i in self.cur.fetchall()]

    # def edit_record(self, table, pos, data):
    #     fields = self.get_fields(table)
    #     # print("fields", fields)
    #     row_id = self.get_all_records(table)[pos][0]
    #     # print(data)
    #     for i in range(len(data)):
    #         if type(self.get_all_records(table)[pos][i]) is str:
    #             data[i] = f"'{data[i]}'"

    #         data[i] = f"{fields[i]}={data[i]}"
    #     data = ', '.join(data)

    def update_record(self, table, position, fields, data):
        row_id = self.get_all_records(table)[position][0]
        set_data = ', '.join([f'{i}={j}' for i, j in zip(fields, data)])
        sql_statement = f"UPDATE {table} SET {set_data} where rowid={row_id}"
        # print(sql_statement)
        self.cur.execute(sql_statement)

    def execute_statement(self, statement):

        self.con.execute("BEGIN TRANSACTION")
        try:
            self.cur.execute(statement)
            self.con.commit()
        except Exception as e:
            self.con.rollback()
            raise e

# with SqliteHandler("./database.db") as sql:

#     sql.add_table("movie", ["title", "year", "score"])
#     sql.add_table("actors", ["age", "oscars", "IQ", "cache"])
#     sql.list_tables()
#     sql.add_records("movie", ["""("Monty Python and the Holy Grail", 1975, 8.2)""",
#                               """("And Now for Something Completely Different", 1971, 7.5)""",
#                               """("Monty Python Live at the Hollywood Bowl", 1982, 7.9)""",
#                               """("Monty Python's The Meaning of Life", 1983, 7.5)""",
#                               """("Monty Python's Life of Brian", 1979, 8.0)"""])
#     #sql.add_records("actors", ["""("Tom Cruise", 2, -10, "2M")"""])
#     #sql.cur.execute("SELECT score FROM movie").fetchall()
#     for record in sql.get_all_records('movie'):
#         print(record)
    #sql.delete_row("movie", 0)
    #print(sql.get_fields('movie'))
    #print(sql.get_record('movie', 10))
    #print(sql.edit_record('movie', 10, ("'edited title'", None, 0)))
    #sql.delete_record('movie', 10)
    #print(sql.get_record('movie', 10))
