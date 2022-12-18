
from database_backend import SqliteHandler
import tkinter as tk
from tkinter import filedialog
from tkinter import ttk
from PIL import ImageTk, Image
from toolbar import Toolbar, ToolbarButton
from treeview_table import TreeviewTable

class Window(tk.Tk):
    def __init__(self, frame, *args):
        tk.Tk.__init__(self)
        self.title("DBManager")
        # self.iconbitmap("icon.ico")
        self.geometry("800x600")
        # self.resizable(False, False)
        


        self.frame = frame(self, *args)
        self.frame.pack(side="top", fill="both", expand=True)

        # self.bind("<Configure>", self.frame.resize)

    def switch_frame(self, frame, *args):
        self.frame.destroy()
        self.frame = frame(self, args)
        self.frame.pack(side="top", fill="both", expand=True)

        # self.bind("<Configure>", self.frame.resize)

class MainFrame(tk.Frame):
    def __init__(self, window: tk.Tk, width, height, background_color):
        tk.Frame.__init__(self, window, width=width, height=height, bg=background_color)
        
        self.window = window
        self.width = width
        self.height = height
        self.database_path = None

        self.window.update()

        self.top_frame = Toolbar(self)
        self.top_frame.grid(row=0, column=0, columnspan=2, sticky="nsew")

        file_button = ToolbarButton(self.window, self.top_frame, text="File")
        file_button.pack(side="left", fill="y")
        file_button.add_button('New', None)
        file_button.add_button('Open', self.open_file)

        edit_button = ToolbarButton(self.window, self.top_frame, text="Edit")
        edit_button.pack(side="left", fill="y")
        edit_button.add_button('Undo', None)
        edit_button.add_button('Redo', None)

        self.left_frame = tk.Frame(self, bg="white", highlightbackground="black", highlightthickness=1)
        self.left_frame.grid(row=1, column=0, sticky="nsew")

        self.table_explorer = ttk.Treeview(self.left_frame)
        self.table_explorer.pack(expand=True, anchor="n", fill="both")

        self.middle_frame = tk.Frame(self, relief=tk.SUNKEN, bg="white", highlightbackground="black", highlightthickness=1)
        self.middle_frame.grid(row=1, column=1, sticky="nsew")

        #add weight to columns and rows
        # self.grid_columnconfigure(0, weight=5)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(1, weight=1)

        self.table = None
    
    # def resize(self, event):
    #     self.window.update()
    #     self.top_frame.config(width=self.window.winfo_width(), height=self.window.winfo_height() * 0.05)
    #     self.left_frame.config(width=self.window.winfo_width() * 0.20, height=self.window.winfo_height() * 0.95)
    #     self.middle_frame.config(width=self.window.winfo_width() * 0.80, height=self.window.winfo_height() * 0.95)
    #     print("resize")

    def open_file(self):
        self.database_path = filedialog.askopenfilename(initialdir="", title="Select File", filetypes=(("DB Files", "*.db"), ("All Files", "*.*")))

        with SqliteHandler(self.database_path) as sql:
            tables = sql.list_tables()

            self.table_explorer.heading("#0", text=self.database_path.split("/")[-1].split(".")[0], anchor=tk.W)

            self.table_explorer.bind("<<TreeviewSelect>>", self.load_table)

            for table in tables:
                self.table_explorer.insert('', 'end', text=table, iid=table)

                for field in sql.get_fields(table):
                    self.table_explorer.insert(table, 'end', text=field, iid=f'{table}-?!£$%^&*{field}')
        
    def load_table(self, event):

        if self.table:
            self.table.destroy()
        
        self.table = TreeviewTable(self.middle_frame)

        with SqliteHandler(self.database_path) as sql:
            table = self.table_explorer.focus()
            table = table.split("-?!£$%^&*")[0]

            self.table.add_fields(sql.get_fields(table))

            records = []

            for record in sql.get_all_records(table):
                records.append(record[1])
            
            self.table.add_records(records)


        self.table.draw()
        self.table.grid(row=0, column=0, sticky="nsew")

window = Window(MainFrame, 800, 600, None)
tk.mainloop()