
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
        self.geometry("1920x1080")

        self.frame = frame(self, *args)
        self.frame.pack(side="top", fill="both", expand=True)

    def switch_frame(self, frame, *args):
        self.frame.destroy()
        self.frame = frame(self, args)
        self.frame.pack(side="top", fill="both", expand=True)

class MainFrame(tk.Frame):
    def __init__(self, window: tk.Tk, width, height, background_color):
        tk.Frame.__init__(self, window, width=width, height=height, bg=background_color)

        # self.changes = {"table_name": [(record_id, (new_data))]}
        self.changes = {}

        self.window = window
        self.width = width
        self.height = height
        self.database_path = None

        self.window.update()

        self.top_frame = Toolbar(self)
        self.top_frame.grid(row=0, column=0, columnspan=2, sticky="nsew")

        file_button = ToolbarButton(self.window, self.top_frame, text="File")
        file_button.pack(side="left", fill="y")
        file_button.add_button('New', self.create_new_file)
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
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(1, weight=1)

        self.table = None
    
    def item_selected(self, event):
        for selected_item in self.table.selection():
            item = self.table.item(selected_item)
            record = item['values']
        
        #get record_number from event
        record_id = record[0]

        #add top level
        top_level = tk.Toplevel(self.window, bg="white")
        top_level.title("Edit Record")
        top_level.geometry("500x500")
        top_level.resizable(False, False)
        top_level.grab_set()
        top_level.focus_set()

        #display record and allow editing
        for i, field in enumerate(self.table.fields):
            label = tk.Label(top_level, text=field, bg="white")
            label.grid(row=i, column=0, sticky="w")

            entry = tk.Entry(top_level)
            entry.grid(row=i, column=1, sticky="w")
            entry.insert(0, record[i])
        
        #add buttons
        save_button = tk.Button(top_level, text="Save", bg="white")
        save_button.grid(row=len(self.table.fields), column=0, sticky="w")

        cancel_button = tk.Button(top_level, text="Cancel", bg="white", command=top_level.destroy)
        cancel_button.grid(row=len(self.table.fields), column=1, sticky="w")
    
    def edit_record_save(self, record_id, new_data):
        if self.table.table_name not in self.changes:
            self.changes[self.table.table_name] = [(record_id, new_data)]
        else:
            self.changes[self.table.table_name].append((record_id, new_data))

    def open_file(self, db=None):
        self.table_explorer.delete(*self.table_explorer.get_children())
        if not db:
            self.database_path = filedialog.askopenfilename(initialdir="", title="Select File", filetypes=(("DB Files", "*.db"), ("All Files", "*.*")))
        else:
            self.database_path = db
        self.table_explorer.heading("#0", text=self.database_path.split("/")[-1].split(".")[0], anchor=tk.W)
        self.table_explorer.bind("<<TreeviewSelect>>", self.load_table)

        with SqliteHandler(self.database_path) as sql:
            tables = sql.list_tables()

        for table in tables:
            self.table_explorer.insert('', 'end', text=table, iid=table)

            for field in sql.get_fields(table):
                self.table_explorer.insert(table, 'end', text=field, iid=f'{table}-?!£$%^&*{field}')
    
    def create_new_file(self):
        file = filedialog.asksaveasfile(filetypes = [('DB File', '*.db*')], defaultextension = [('DB File', '*.db*')])
        self.open_file(db=file)
        
    def load_table(self, event):

        if self.table:
            self.table.destroy()
        
        self.table = TreeviewTable(self.middle_frame)
        self.table.bind("<<TreeviewSelect>>", self.item_selected)

        with SqliteHandler(self.database_path) as sql:
            table = self.table_explorer.focus()
            table = table.split("-?!£$%^&*")

            if len(table) == 1:                
                self.table.add_fields(sql.get_fields(table[0]))

                records = []

                for record in sql.get_all_records(table[0]):
                    records.append(record)
                    
                self.table.add_records(records)
            
            elif len(table) == 2:
                fields = sql.get_fields(table[0])
                field = table[1]

                self.table.add_fields([field])

                records = []

                for record in sql.get_all_records(table[0]):
                    records.append([record[fields.index(field)]])
                
                self.table.add_records(records)

        self.table.draw()
        self.table.grid(row=0, column=0, sticky="nsew")
        self.middle_frame.grid_columnconfigure(0, weight=1)
        self.middle_frame.grid_rowconfigure(0, weight=1)

window = Window(MainFrame, 800, 600, None)
tk.mainloop()
