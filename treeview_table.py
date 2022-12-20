import tkinter as tk
from tkinter import ttk
from tkinter.messagebox import showinfo

class TreeviewTable(ttk.Treeview):
    def __init__(self, master):
        super().__init__(master, show='headings')

        self.fields = []
        self.records = []

        #add scrollbar
        self.scrollbar_y = ttk.Scrollbar(master, orient=tk.VERTICAL, command=self.yview)
        self.configure(yscroll=self.scrollbar_y.set)
        self.scrollbar_y.grid(row=0, column=1, sticky='ns')

        self.scrollbar_x = ttk.Scrollbar(master, orient=tk.HORIZONTAL, command=self.xview)
        self.configure(xscroll=self.scrollbar_x.set)
        self.scrollbar_x.grid(row=1, column=0, sticky='ew')

    def add_selected_item_callback(self, callback):
        self.bind('<<TreeviewSelect>>', callback)

    def add_records(self, records: tuple):
        self.records.extend(records)
    
    def add_fields(self, fields: tuple):
        self.configure(columns=('row_number', *fields))
        self.fields.extend(fields)
    
    def draw(self):
        # define headings

        #add row number
        self.heading('#0', text='Row number', anchor=tk.W)
        self.column('#0', width = int(1920 * 0.05))

        for field in self.fields:
            self.heading(field, text=field)
            # print("field", field)
        
        # add data to the treeview
        row_number = 0
        for record in self.records:
            self.insert('', tk.END, values=(row_number, *record))
            row_number += 1

        # print(self.records)

# window = tk.Tk()
# window.title('Treeview demo')
# window.geometry('620x200')

# table = TreeviewTable(window)
# table.add_fields(('first_name', 'last_name', 'email'))

# records = []

# for i in range(10):
#     records.append((f'first {i}', f'last {i}', f'email{i}@gmail.com'))

# table.add_records(records)

# table.draw()
# table.grid(row=0, column=0, sticky='nsew')

# tk.mainloop()

