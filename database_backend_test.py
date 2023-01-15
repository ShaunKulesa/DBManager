from database_backend import SqliteHandler

sql = SqliteHandler("chinook.db")
#drop table "test"
# sql.cur.execute("DROP TABLE IF EXISTS test")

# sql.begin()
# sql.add_table("test", ("id INTEGER PRIMARY KEY", "name TEXT", "age INTEGER"))
# sql.add_records("test", (1, "John", 20))
# sql.add_records("test", (2, "Jane", 21))
# sql.add_records("test", (3, "Jack", 22))
# sql.add_records("test", (4, "Jill", 23))
# sql.add_records("test", (5, "Jen", 24))
# sql.add_records("test", (6, "Jenny", 25))
# sql.end()

print(sql.get_all_records("test"))

  