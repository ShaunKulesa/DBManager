from database_backend import SqliteHandler
import tkinter as tk
from tkinter import filedialog, ttk
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
        self.frame = frame(self, *args)
        self.frame.pack(side="top", fill="both", expand=True)

class MainFrame(tk.Frame):
    def __init__(self, window: tk.Tk, width, height, background_color):
        tk.Frame.__init__(self, window, width=width, height=height, bg=background_color)

        # self.changes = {"table_name": [("update", record_id, (new_data)) or ("insert", record_id, (new_data)) or ("delete", record_id, (new_data))]}
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



        self.middle_frame = tk.Frame(self, relief=tk.SUNKEN, bg="white", highlightbackground="black", highlightthickness=1)
        self.middle_frame.grid(row=1, column=1, sticky="nsew")

        #add weight to columns and rows
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(1, weight=1)

        self.table = None
        self.table_explorer = None
        self.top_level = None
    
    def item_selected(self, event):
        for selected_item in self.table.selection():
            item = self.table.item(selected_item)
            record_id = item['values'][0]
            record = item['values'][1:]
            fields = list(self.table.fields)

        #add top level
        if not self.top_level:
            self.top_level = tk.Toplevel(self.window, bg="white")
            self.top_level.title("Edit Record")
            #top_level.geometry("500x500")
            self.top_level.resizable(False, False)
            self.top_level.focus_set()
        
        entries = []
        
        style = ttk.Style()

        # remove the dashed line from Tabs
        style.configure("Tab", focuscolor=style.configure(".")["background"])

        tabControl = ttk.Notebook(self.top_level, takefocus=False)
        edit_record_tab = ttk.Frame(tabControl, takefocus=False)
        padding = max([len(field) for field in self.table.fields])
        
        #display record and allow editing
        for i, field in enumerate(self.table.fields):
            label = tk.Label(edit_record_tab, text=field+" "*(padding-len(field)), bg="white", font=("Consolas", 14))
            label.grid(row=i, column=0, sticky="w", padx=5, pady=2)

            entry = tk.Entry(edit_record_tab, justify='left', font=("Consolas", 14))
            entry.grid(row=i, column=1, sticky="w", padx=5, pady=2)
            entry.insert(0, record[i])

            entries.append(entry)
        
        #add buttons
        save_button = tk.Button(edit_record_tab, text="Save", bg="white", command=lambda: self.edit_record(record_id, fields, [entry.get() for entry in entries]))
        save_button.grid(row=len(self.table.fields), column=0)

        cancel_button = tk.Button(edit_record_tab, text="Cancel", bg="white", command=self.top_level.destroy)
        cancel_button.grid(row=len(self.table.fields), column=1)

        tabControl.add(edit_record_tab, text="Edit Record")


        #add tab for deleting record
        delete_record_tab = ttk.Frame(tabControl, takefocus=False)

        delete_button = tk.Button(delete_record_tab, text="Delete Record", bg="red", command=lambda: self.delete_record(record_id))
        delete_button.grid(row=0, column=0, sticky="w")

        tabControl.add(delete_record_tab, text="Delete Record")

        tabControl.pack(expand=1, fill="both")

        
    def edit_record(self, record_id, fields, new_data):
        with SqliteHandler(self.database_path) as sql:
            record = list(sql.get_record(self.table.name, record_id))
            
            for field in fields:
                record[sql.get_fields(self.table.name).index(field)] = new_data[0]
                new_data.pop(0)

            self.changes[self.table.name].append(("update", record_id, record))
            self.load_table()
    
    def delete_record(self, record_id):
        with SqliteHandler(self.database_path) as sql:
            self.changes[self.table.name].append(("delete", record_id, sql.get_record(self.table.name, record_id)))
            self.load_table()
 
    def open_file(self, db=None):
        if not db:
            self.database_path = filedialog.askopenfilename(initialdir="", title="Select File", filetypes=(("DB Files", "*.db"), ("All Files", "*.*")))
        else:
            self.database_path = db

        self.table_explorer = ttk.Treeview(self.left_frame)
        self.table_explorer.pack(expand=True, anchor="n", fill="both")
        
        self.table_explorer.heading("#0", text=self.database_path.split("/")[-1].split(".")[0], anchor=tk.W)
        self.table_explorer.bind("<<TreeviewSelect>>", self.load_table)

        with SqliteHandler(self.database_path) as sql:
            tables = sql.list_tables()

            for table in tables:
                self.table_explorer.insert('', 'end', text=table, iid=table)

                for field in sql.get_fields(table):
                    self.table_explorer.insert(table, 'end', text=field, iid=f'{table}-?!£$%^&*{field}')
        
        #add tables to changes
        for table in tables:
            self.changes[table] = []
    
    def create_new_file(self):
        file = filedialog.asksaveasfile(filetypes = [('DB File', '*.db*')], defaultextension = [('DB File', '*.db*')])
        self.open_file(db=file)
        
    def load_table(self, event=None):
        if self.table:
            self.table.destroy()
        
        table_name = self.table_explorer.focus().split("-?!£$%^&*")

        self.table = TreeviewTable(self.middle_frame, table_name[0])
        self.table.bind("<Double-Button-1>", self.item_selected)

        with SqliteHandler(self.database_path) as sql:
            if len(table_name) == 1:                
                self.table.add_fields(sql.get_fields(table_name[0]))

                records = []

                for record in sql.get_all_records(table_name[0]):
                    records.append(record)
                
                for i in self.changes[table_name[0]]:
                    if i[0] == "update":
                        records[i[1]] = i[2]
                    elif i[0] == "delete":
                        records.pop(i[1])
            
            elif len(table_name) == 2:
                fields = sql.get_fields(table_name[0])
                field = table_name[1]

                self.table.add_fields([field])

                records = []

                for record in sql.get_all_records(table_name[0]):
                    records.append([record[fields.index(field)]])
                
                for i in self.changes[table_name[0]]:
                    if i[0] == "update":
                        records[i[1]][0] = i[2][fields.index(field)]
                    elif i[0] == "delete":
                        records.pop(i[1])
                
            

            self.table.add_records(records)

        self.table.draw()
        self.table.grid(row=0, column=0, sticky="nsew")
        self.middle_frame.grid_columnconfigure(0, weight=1)
        self.middle_frame.grid_rowconfigure(0, weight=1)

window = Window(MainFrame, 800, 600, "red")
tk.mainloop()
