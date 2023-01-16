from database_backend import SqliteHandler
import tkinter as tk
from tkinter import filedialog, ttk
from toolbar import Toolbar, ToolbarButton
from treeview_table import TreeviewTable
import sys

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

        self.window = window
        self.width = width
        self.height = height
        self.database_path: str = None
        self.table_transactions = {} # {table_name: [('delete_record', row_number: int), ('delete_records', row_numbers_slice: slice), (update_record, row_number: int, new_data: tuple)]}

        self.window.update()

        self.top_frame = Toolbar(self)
        self.top_frame.grid(row=0, column=0, columnspan=3, sticky="nsew")

        file_button = ToolbarButton(self.window, self.top_frame, text="File")
        file_button.pack(side="left", fill="y")
        file_button.add_button('New', self.create_new_file)
        file_button.add_button('Open', self.open_file)

        edit_button = ToolbarButton(self.window, self.top_frame, text="Edit")
        edit_button.pack(side="left", fill="y")
        edit_button.add_button('Undo', None)
        edit_button.add_button('Redo', None)

        self.left_frame = tk.Frame(self, highlightbackground="white", highlightthickness=1)
        self.left_frame.grid(row=1, column=0, sticky="nsew")

        self.middle_frame = tk.Frame(self, relief=tk.SUNKEN)
        self.middle_frame.grid(row=1, column=1, sticky="nsew")

        self.right_frame = tk.Frame(self, highlightbackground="white", highlightthickness=1)
        self.right_frame.grid(row=1, column=2, sticky="nsew")

        self.fields_frame = tk.LabelFrame(self.right_frame, text="Record", highlightthickness=1)
        self.fields_frame.grid(row=0, column=0, columnspan=2, sticky="nsew")

        self.save_button = tk.Button(self.right_frame, text="Save", state="disabled")
        self.save_button.grid(row=1, column=0, sticky="nsew")

        self.delete_button = tk.Button(self.right_frame, text="Delete", state="disabled")
        self.delete_button.grid(row=1, column=1, sticky="nsew")

        self.sql_console = tk.Text(self.right_frame, bg="white")
        self.sql_console.grid(row=2, column=0, columnspan=2, sticky="nsew")

        self.right_frame.grid_rowconfigure(0, weight=1, uniform="fields_frame")
        self.right_frame.grid_rowconfigure(2, weight=2, uniform="fields_frame")
        self.right_frame.grid_columnconfigure(0, weight=1, uniform="fields_frame")
        self.right_frame.grid_columnconfigure(1, weight=1, uniform="fields_frame")

        #add weight to columns and rows
        self.grid_columnconfigure(0, weight=1, uniform="group1")
        self.grid_columnconfigure(1, weight=8, uniform="group1")
        self.grid_columnconfigure(2, weight=2, uniform="group1")
        self.grid_rowconfigure(1, weight=1, uniform="group1")

        self.table = None
        self.table_explorer = None

    def select_next_item(self):
        next_item = self.table.next(self.table.selection()[0])
        self.table.selection_set(next_item)
        self.item_selected()

    def select_prev_item(self):
        prev_item = self.table.prev(self.table.selection()[0])
        self.table.selection_set(prev_item)
        self.item_selected()

    def item_selected(self, event=None):
        item:tuple = self.table.item(self.table.selection()[0])
        record_id = item['values'][0]
        record = item['values'][1:]

        entries = []

        #delete all widgets in fields_frame
        for widget in self.fields_frame.winfo_children():
            widget.destroy()
        
        #add field labels
        for i, field in enumerate(self.table.fields):
            field_label = tk.Label(self.fields_frame, text=field, bg="white", anchor="w")
            field_label.grid(row=i, column=0, sticky="nsew")
        
        #add field entries
        for i, field in enumerate(record):
            entry = tk.Entry(self.fields_frame, bg="white")
            entry.insert(0, field)
            entry.grid(row=i, column=1, sticky="nsew")
            entry.bind('<Return>', lambda x:self.save_button.invoke())
            entries.append(entry)
        
        self.fields_frame.grid_columnconfigure(0, weight=1, uniform="fields_frame")
        self.fields_frame.grid_columnconfigure(1, weight=4, uniform="fields_frame")

        field_positions = []
        for field in self.table.fields:
            with SqliteHandler(self.database_path) as sql:
                if field in sql.get_fields(self.table.name):
                    field_positions.append(self.table.fields.index(field))

        self.save_button.config(command=lambda: self.update_record(self.table.name, record_id, list(record[:field_positions[0]] + [entries[i].get() for i in field_positions] + record[field_positions[-1]+1:])), state="normal")
        self.delete_button.config(command=lambda: self.delete_record(self.table.name, record_id), state="normal")

    def update_record(self, table_name, row_number, data):
        self.table_transactions[table_name].append(('update_record', row_number, data))

        # reload the table widget
        self.load_table()

    def delete_record(self, table_name, row_number: int):
        self.table_transactions[table_name].append(('delete_record', row_number))

        # reload the table widget
        self.load_table()

        #clear fields_frame
        for widget in self.fields_frame.winfo_children():
            widget.destroy()

        #disable buttons
        self.save_button.config(state="disabled")
        self.delete_button.config(state="disabled")
    
    def delete_records(self, table_name, row_numbers_slice: slice):
        self.table_transactions[table_name].append(('delete_records', row_numbers_slice))

        # reload the table widget
        self.load_table()

        #clear fields_frame
        for widget in self.fields_frame.winfo_children():
            widget.destroy()

        #disable buttons
        self.save_button.config(state="disabled")
        self.delete_button.config(state="disabled")
 
    def open_file(self, db=None):
        if not db:
            db = filedialog.askopenfilename(initialdir="", title="Select File", filetypes=(("DB Files", "*.db"), ("All Files", "*.*")))
        self.database_path = db

        if not self.table_explorer:
            self.table_explorer = ttk.Treeview(self.left_frame)
            self.table_explorer.pack(expand=True, anchor="n", fill="both")
            self.table_explorer.bind("<<TreeviewSelect>>", self.load_table)
        else:
            self.table_explorer.delete(*self.table_explorer.get_children())

        self.table_explorer.heading("#0", text=self.database_path.split("/")[-1].split(".")[0], anchor=tk.W)
        
        with SqliteHandler(self.database_path) as sql:
            tables = sql.list_tables()

            for table in tables:
                #table iid = ['table_name']
                self.table_explorer.insert('', 'end', text=table, iid=f'[{table}]')

                for field in sql.get_fields(table):
                    #field iid = ['table_name', 'field_name']
                    self.table_explorer.insert(f'[{table}]', 'end', text=field, iid=f'[{table}, {field}]')
        
        #add tables to changes
        for table in tables:
            self.table_transactions[table] = []
    
    def create_new_file(self):
        file = filedialog.asksaveasfile(filetypes = [('DB File', '*.db*')], defaultextension = [('DB File', '*.db*')])
        self.open_file(db=file.name)
    
    def table_popup(self, event=None):
        #set table selection as iid if the target item is not seleccted with left click
        iid = self.table.identify_row(event.y)
        if iid not in self.table.selection():
            self.table.selection_set(iid)

        # loop through items and get their value
        items_iid = self.table.selection()
        items_values = [] # items values = [[rownumber, *record data]]

        for iid in items_iid:
            items_values.append(self.table.item(iid)['values'])

        #create popup menu
        popup = tk.Frame(self.master)
        popup.place(x=event.x_root, y=event.y_root)

        #add buttons
        delete_button = tk.Button(popup, text="Delete", command=lambda: self.delete_records(self.table.name, slice(items_values[0][0], items_values[-1][0]+1)))
        delete_button.pack()
  
    def load_table(self, event=None):
        if self.table:
            self.table.destroy()

        #clear fields_frame
        for widget in self.fields_frame.winfo_children():
            widget.destroy()

        # get table name or table name and field name
        selection = self.table_explorer.focus().strip('][').split(', ')

        self.table = TreeviewTable(self.middle_frame, selection[0])
        self.table.bind("<<TreeviewSelect>>", self.item_selected)
        self.table.bind("<Button-3>", self.table_popup)
        
        with SqliteHandler(self.database_path) as sql:
            for transaction in self.table_transactions[selection[0]]:
                if transaction[0] == 'delete_record':
                    print(transaction[1])
                    sql.delete_record(selection[0], transaction[1])
                
                elif transaction[0] == 'delete_records':
                    sql.delete_records(selection[0], transaction[1])
                
                elif transaction[0] == 'update_record':
                    print(transaction[1], transaction[2])
                    sql.edit_record(selection[0], transaction[1], transaction[2])
            
            records = sql.get_all_records(selection[0])
            print(records)
            fields = sql.get_fields(selection[0])
        
        
        self.table.add_records(records)
        self.table.add_fields(fields)

        self.table.draw()
        self.table.grid(row=0, column=0, sticky="nsew")
        self.middle_frame.grid_columnconfigure(0, weight=1)
        self.middle_frame.grid_rowconfigure(0, weight=1)

window = Window(MainFrame, 800, 600, "red")
tk.mainloop()
