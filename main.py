from table import Table, Header, Record
from database_backend import SqliteHandler
from tkinter import *
from tkinter import filedialog
from tkinter import ttk

class Window(Tk):
    def __init__(self, frame, *args):
        Tk.__init__(self)
        self.title("DBManager")
        self.geometry("800x600")

        self.frame = frame(self, *args)
        self.frame.pack()
    
    def switch_frame(self, frame, *args):
        self.frame.destroy()
        self.frame = frame(self, args)
        self.frame.pack()

class MainFrame(Frame):
    def __init__(self, window, width, height, background_color):
        Frame.__init__(self, window, width=width, height=height, bg=background_color)
        self.window = window
        self.width = width
        self.height = height

        self.database_path = None

        m1 = PanedWindow(orient=VERTICAL)
        m1.pack(fill=BOTH)

        top_frame = Frame(m1, height=600 * 0.20, width=800, relief=SUNKEN, bg="red")
        m1.add(top_frame)

        open_file_button = Button(top_frame, text="Open File", command=lambda: self.open_file())
        open_file_button.pack()

        m2 = PanedWindow(m1, orient=HORIZONTAL)
        m1.add(m2)

        left_frame = Frame(m2, height=600, width=800 * 0.20, relief=SUNKEN, bg="blue")
        m2.add(left_frame)

        self.table_explorer = ttk.Treeview(left_frame)
        self.table_explorer.pack()

        self.middle_frame = Frame(m2, height=600, width=800 * 0.60, relief=SUNKEN, bg="green")
        m2.add(self.middle_frame)
    
    def open_file(self):
        file_explorer = filedialog.askopenfilename(initialdir="/", title="Select File", filetypes=(("DB Files", "*.db"), ("All Files", "*.*")))
        self.database_path = file_explorer

        with SqliteHandler(self.database_path) as sql:
            tables = sql.list_tables()

            self.table_explorer.heading("#0", text=self.database_path.split("/")[-1].split(".")[0], anchor=W)

            self.table_explorer.bind("<<TreeviewSelect>>", self.load_table)


            for table in tables:
                self.table_explorer.insert('', 'end', text=table, iid=table)

                for field in sql.get_fields(table):
                    self.table_explorer.insert(table, 'end', text=field, iid=f'{table}-?!£$%^&*{field}')
        
    
    def load_table(self, event):
        self.table = Table(self.middle_frame, self.database_path.split("/")[-1].split(".")[0])

        with SqliteHandler(self.database_path) as sql:
            table = self.table_explorer.focus()
            table = table.split("-?!£$%^&*")[0]

            print(table)

            print(sql.get_fields(table))
            header = Header(self.table, sql.get_fields(table))
            self.table.add_header(header)

            for record in sql.get_all_records(table):
                self.table.add_records([Record(self.table, record[1])])

            # print(sql.get_all_records(table))


        self.table.draw()

window = Window(MainFrame, 800, 600, None)
mainloop()