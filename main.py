from table import Table, Header, Record
from database_backend import SqliteHandler
from tkinter import *
from tkinter import filedialog
from tkinter import ttk
from PIL import ImageTk, Image

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

        top_frame = Frame(self.window, relief=SUNKEN, width = self.window.winfo_width(), height = self.window.winfo_height() * 0.10, bg="#E78587",)
        top_frame.pack_propagate(0)
        top_frame.pack(side = TOP)
        
        self.open_folder_icon = ImageTk.PhotoImage(Image.open("open_file_icon.png").resize((40, 40)))
        open_folder_button = Button(top_frame, image=self.open_folder_icon, command=lambda: self.open_file(), width=100, height=100)
        open_folder_button.pack(side=LEFT)

        left_frame = Frame(self.window, width = self.window.winfo_width() * 0.20, height = self.window.winfo_height() * 0.90, bg="#E78587", highlightbackground="black", highlightthickness=1)
        left_frame.pack_propagate(0)
        left_frame.pack(side = LEFT)

        self.table_explorer = ttk.Treeview(left_frame)
        self.table_explorer.pack(expand=True, fill=BOTH)

        self.middle_frame = Frame(self.window, relief=SUNKEN, width = self.window.winfo_width() * 0.90,height = self.window.winfo_height() * 0.90)
        self.middle_frame.pack_propagate(0)
        self.middle_frame.pack(side = LEFT)
    
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