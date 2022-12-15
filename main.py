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
    def __init__(self, window: Tk, width, height, background_color):
        Frame.__init__(self, window, width=width, height=height, bg=background_color)
        
        self.window = window
        self.width = width
        self.height = height
        self.database_path = None

        self.window.update()

        m1 = PanedWindow(orient=VERTICAL, bg='blue')
        m1.pack(fill=BOTH)

        top_frame = Frame(m1, relief=SUNKEN, width = self.window.winfo_width(), height = self.window.winfo_height() * 0.10)
        top_frame.pack_propagate(0)
        m1.add(top_frame)

        open_file_button = Button(top_frame, text="Open File", command=lambda: self.open_file())
        open_file_button.pack()

        m2 = PanedWindow(m1, orient=HORIZONTAL, bg='red')
        m2.pack(fill=BOTH, expand=True)
        m1.add(m2)

        left_frame = Frame(m2, width = self.window.winfo_width() * 0.20, height = self.window.winfo_height() * 0.90, relief=SUNKEN)
        left_frame.pack_propagate(0)
        left_frame.pack(fill=BOTH, expand=True)
        m2.add(left_frame)

        self.table_explorer = ttk.Treeview(left_frame)
        self.table_explorer.pack(expand=True, fill=BOTH)

        self.middle_frame = Frame(m2, relief=SUNKEN, width = self.window.winfo_width() * 0.90,height = self.window.winfo_height() * 0.90)
        self.middle_frame.pack_propagate(0)
        self.middle_frame.pack(fill=BOTH, expand=True)
        m2.add(self.middle_frame)
    
    def open_file(self):
        self.database_path = filedialog.askopenfilename(initialdir="/", title="Select File", filetypes=(("DB Files", "*.db"), ("All Files", "*.*")))

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

            header = Header(self.table, sql.get_fields(table))
            self.table.add_header(header)

            for record in sql.get_all_records(table):
                self.table.add_records([Record(self.table, record[1])])

        self.table.draw()
        self.table.frame.pack(side=LEFT, fill=BOTH, expand=True)

window = Window(MainFrame, 800, 600, None)
mainloop()