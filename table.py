from tkinter import *
import time
from database_backend import Sqlite_handler


start = time.perf_counter()

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
    def __init__(self, table_name):
        self.records = []
        # self.canvas = Canvas()
        # self.canvas.pack(anchor='center')
        self.table_name = table_name

        self.column_widths = []

        frame=Frame(root,width=300,height=300)
        frame.pack(expand=True, fill=BOTH) #.grid(row=0,column=0)
        self.canvas=Canvas(frame,bg='#FFFFFF',width=300,height=300,scrollregion=(0,0,10000,10000))
        hbar=Scrollbar(frame,orient=HORIZONTAL)
        hbar.pack(side=BOTTOM,fill=X)
        hbar.config(command=self.canvas.xview)
        vbar=Scrollbar(frame,orient=VERTICAL)
        vbar.pack(side=RIGHT,fill=Y)
        vbar.config(command=self.canvas.yview)
        self.canvas.config(width=300,height=300)
        self.canvas.config(xscrollcommand=hbar.set, yscrollcommand=vbar.set)
        self.canvas.pack(side=LEFT,expand=True,fill=BOTH)
    
    def add_header(self, header: Header):
        self.header = header
        self.name = header.get_name()
        self.columns = header.get_columns()
    
    def add_records(self, records: tuple):
        self.records.extend(records)

    def draw(self):
        # print(self.records)
        #maths
        for column_counter in range(len(self.columns)):
            widths = []
            widths.append(self.header.get_text_width(column_counter))
            for record in self.records:
                widths.append(record.get_text_width(column_counter))
            self.column_widths.append(max(widths))
        record_width = sum(self.column_widths)
        print(self.column_widths)

        header_height = self.header.get_height()

        self.canvas.create_rectangle(0, 0, record_width, header_height + (30 * len(self.records)), fill=self.header.fill_color, outline=self.header.outline_color, width=self.header.outline_width)

        self.canvas.config(width=record_width, height=header_height + (header_height * len(self.records)))

        # draw header with centered text
        for column_counter in range(len(self.columns)):
            self.canvas.create_text(sum(self.column_widths[:column_counter]) + (self.column_widths[column_counter] / 2), header_height / 2, text=self.columns[column_counter])

        # draw records with centered text
        for record_counter in range(len(self.records)):
            self.canvas.create_line(0, header_height + (header_height * record_counter), record_width, header_height + (header_height * record_counter), fill='#D3D3D3')
            for column_counter in range(len(self.columns)):
                self.canvas.create_text(sum(self.column_widths[:column_counter]) + (self.column_widths[column_counter] / 2), header_height + (header_height * record_counter) + (header_height / 2), text=self.records[record_counter].data[column_counter])
root = Tk()

table = Table('Person')
header = Header(table, ['firstName', 'lastName', 'Age'])
table.add_header(header)
table.add_records([Record(table, ['Shaun', 'Kulesa', 17,])] * 1000)
# table.add_records([Record(table, ['John', 'Doe', 20,])] * 100)

table.draw()

# with Sqlite_handler("chinook.db") as db:
#     table = Table('Albums')
#     header = Header(table, db.get_fields('albums'))
#     table.add_header(header)
#     table.add_records([Record(table, record[1]) for record in db.get_all_rows('albums')])
#     # table.add_records([print(record) for record in db.get_all_rows('albums')])

#     table.draw()



        
finish = time.perf_counter()
print(f'Finished in {round(finish-start, 2)} second(s)')

mainloop()
