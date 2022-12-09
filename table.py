from tkinter import *
import time
from database_backend import SqliteHandler


# start = time.perf_counter()

class Header:
    def __init__(self, table, data=[], outline_color='black', fill_color='white', outline_width=0):
        self.table = table
        self.table_name = table.table_name
        self.data = data
        self.outline_color = outline_color
        self.fill_color = fill_color
        self.outline_width = outline_width
    
    def get_name(self):
        return self.table_name
    
    def get_columns(self):
        return self.data
    
    def get_text_width(self, column):
        text = Label(text=self.data[column])
        return text.winfo_reqwidth()
    
    def get_height(self):
        tallest_text = 0
        for text in self.data:
            text = Label(text=text)
            if text.winfo_reqheight() > tallest_text:
                tallest_text = text.winfo_reqheight()
            
        return tallest_text + (self.outline_width * 2)

class Record:
    def __init__(self, table, data=[], outline_color='black', fill_color='white', outline_width=0):
        self.table = table
        self.data = data
        self.outline_color = outline_color
        self.fill_color = fill_color
        self.outline_width = outline_width

    def get_text_width(self, column):
        text = Label(text=self.data[column])
        return text.winfo_reqwidth()

    def get_height(self):
        tallest_text = 0
        for text in self.data:
            text = Label(text=text)
            if text.winfo_reqheight() > tallest_text:
                tallest_text = text.winfo_reqheight()
         
        return tallest_text + (self.outline_width * 2)

class Table:
    def __init__(self, parent, table_name):
        self.records = []
        self.table_name = table_name

        self.column_widths = []

        frame=Frame(parent, width=300,height=300)
        frame.pack(anchor='center') #.grid(row=0,column=0)
        self.canvas=Canvas(frame,bg='#FFFFFF',width=300,height=300)
        hbar=Scrollbar(frame,orient=HORIZONTAL)
        hbar.pack(side=BOTTOM,fill=X)
        hbar.config(command=self.canvas.xview)
        vbar=Scrollbar(frame,orient=VERTICAL)
        vbar.pack(side=RIGHT,fill=Y)
        vbar.config(command=self.canvas.yview)
        self.canvas.config(width=300,height=300)
        self.canvas.config(xscrollcommand=hbar.set, yscrollcommand=vbar.set)
        self.canvas.pack(expand=True,fill=BOTH, anchor='center')
    
    def add_header(self, header: Header):
        self.header = header
        self.name = header.get_name()
        self.columns = header.get_columns()
    
    def add_records(self, records: tuple):
        self.records.extend(records)

    def draw(self):
        #maths
        for column_counter in range(len(self.columns)):
            widths = []
            widths.append(self.header.get_text_width(column_counter))
            for record in self.records:
                widths.append(record.get_text_width(column_counter))
            self.column_widths.append(max(widths))
        record_width = sum(self.column_widths)
        row_number_width = Label(text=str(len(self.records))).winfo_reqwidth()
        header_height = self.header.get_height()

        print(row_number_width)
        print(record_width)
        print(self.column_widths)
        
        self.canvas.create_rectangle(2, 2, record_width + row_number_width, (header_height + (header_height * len(self.records))) - 2, fill=self.header.fill_color, outline="black", width=1)

        self.canvas.config(width=record_width + row_number_width, height=header_height + (header_height * len(self.records)), scrollregion=(2, 2, record_width + row_number_width, (header_height + (header_height * len(self.records)))))

        # draw row number background
        self.canvas.create_rectangle(3, header_height, row_number_width, header_height + (header_height * len(self.records)) - 2, fill='light grey', width=0)

        #draw row numbers
        for row_counter in range(len(self.records)):
            self.canvas.create_text((row_number_width/2), header_height + (row_counter * self.records[row_counter].get_height()) + (self.records[row_counter].get_height()/2), text=str(row_counter + 1), anchor='center')
        
        # row number column line
        self.canvas.create_line(row_number_width, 2, row_number_width, (header_height + (header_height * len(self.records))) - 2, fill=self.header.outline_color, width=self.header.outline_width)

        #column lines
        column_line_x = row_number_width
        for column_counter in range(len(self.columns) - 1):
            column_line_x += self.column_widths[column_counter]
            self.canvas.create_line(column_line_x, 2, column_line_x, header_height + (header_height * len(self.records)) - 2, fill=self.header.outline_color, width=self.header.outline_width)

        # draw header with centered text
        for column_counter in range(len(self.columns)):
            self.canvas.create_text(sum(self.column_widths[:column_counter]) + row_number_width + 2, header_height / 2, text=self.columns[column_counter], anchor='w')

        # draw records with centered text
        for record_counter in range(len(self.records)):
            self.canvas.create_line(row_number_width + 1, header_height + (header_height * record_counter), record_width + row_number_width + 1, header_height + (header_height * record_counter), fill='#D3D3D3')
            for column_counter in range(len(self.columns)):
                self.canvas.create_text(sum(self.column_widths[:column_counter]) + row_number_width + 2, header_height + (header_height * record_counter) + (header_height / 2), text=self.records[record_counter].data[column_counter], anchor='w')
# root = Tk()

# with SqliteHandler("chinook.db") as db:
#     table = Table(root, 'albums')
#     # print(db.list_tables())
#     header = Header(table, db.get_fields('albums'))
#     print(db.get_fields('albums'))
#     table.add_header(header)
#     table.add_records([Record(table, record[1]) for record in db.get_all_records('albums')])
#     table.draw()

# finish = time.perf_counter()
# # print(f'Finished in {round(finish-start, 2)} second(s)')

# mainloop()
