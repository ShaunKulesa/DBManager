from table import Table, Header, Record
from database_backend import SqliteHandler
import tkinter as tk
from tkinter import filedialog
from tkinter import ttk
from PIL import ImageTk, Image
from toolbar import Toolbar, ToolbarButton

class Window(tk.Tk):
    def __init__(self, frame, *args):
        tk.Tk.__init__(self)
        self.title("DBManager")
        self.geometry("800x600")

        self.frame = frame(self, *args)
        self.frame.pack()
    
    def switch_frame(self, frame, *args):
        self.frame.destroy()
        self.frame = frame(self, args)
        self.frame.pack()

class MainFrame(tk.Frame):
    def __init__(self, window: tk.Tk, width, height, background_color):
        tk.Frame.__init__(self, window, width=width, height=height, bg=background_color)
        
        self.window = window
        self.width = width
        self.height = height
        self.database_path = None

        self.window.update()

        self.header_frame = tk.Frame()
        self.header_frame.pack()

        self.header_frame.update()
        
        top_frame = Toolbar(self.header_frame, self.window.winfo_width(), self.window.winfo_height() * 0.05)
        top_frame.pack_propagate(0)
        top_frame.pack(side="top", anchor="nw")

        file_button = ToolbarButton(self.window, top_frame, text="File")
        file_button.pack(side="left", fill="y")
        file_button.add_button('New')
        file_button.add_button('Open')

        edit_button = ToolbarButton(self.window, top_frame, text="Edit")
        edit_button.pack(side="left", fill="y")
        edit_button.add_button('Undo')
        edit_button.add_button('Redo')

        self.body_frame = tk.Frame()
        self.body_frame.pack()

        left_frame = tk.Frame(self.body_frame, width = self.window.winfo_width() * 0.20, height = self.window.winfo_height() * 0.90, bg="#E78587", highlightbackground="black", highlightthickness=1)

        left_frame.pack(side="left")

        self.table_explorer = ttk.Treeview(left_frame)
        self.table_explorer.pack(expand=True, fill=tk.BOTH)

        self.middle_frame = tk.Frame(self.body_frame, relief=tk.SUNKEN, width = self.window.winfo_width() * 0.90,height = self.window.winfo_height() * 0.90, bg="blue", highlightbackground="black", highlightthickness=1)
        self.middle_frame.pack(side="left")


    
    def open_file(self):
        self.database_path = filedialog.askopenfilename(initialdir="/", title="Select File", filetypes=(("DB Files", "*.db"), ("All Files", "*.*")))

        with SqliteHandler(self.database_path) as sql:
            tables = sql.list_tables()

            self.table_explorer.heading("#0", text=self.database_path.split("/")[-1].split(".")[0], anchor=tk.W)

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
        self.table.frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

window = Window(MainFrame, 800, 600, None)
tk.mainloop()