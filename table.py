from tkinter import *
import time
from database_backend import SqliteHandler
import tkinter.font as tkfont

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
    
    def get_text_width(self, column, test_label):
        test_label.config(text=self.data[column])
        width = test_label.winfo_reqwidth()
        return width
    
    def get_height(self, test_label):
        tallest_text = 0
        for text in self.data:
            test_label.config(text=text)
            if test_label.winfo_reqheight() > tallest_text:
                tallest_text = test_label.winfo_reqheight()
            
        return tallest_text + (self.outline_width * 2)

class Record:
    def __init__(self, table, data=[], outline_color='black', fill_color='white', outline_width=0):
        self.table = table
        self.data = data
        self.outline_color = outline_color
        self.fill_color = fill_color
        self.outline_width = outline_width

    def get_text_width(self, column, test_label):
        test_label.config(text=self.data[column])
        return test_label.winfo_reqwidth()
        

    def get_height(self, test_label):
        tallest_text = 0
        for text in self.data:
            test_label.config(text=text)
            if test_label.winfo_reqheight() > tallest_text:
                tallest_text = test_label.winfo_reqheight()
         
        return tallest_text + (self.outline_width * 2)

    # def get_text_width(self, column):
    #    return tkfont.Font(family="Consolas", size=10, weight="normal").measure(self.data[column])
    
class Table:
    def __init__(self, parent, table_name):
        self.records = []
        self.table_name = table_name

        self.column_widths = []

        self.frame=Frame(parent)
        # frame.pack(anchor='center') #.grid(row=0,column=0)
        self.canvas=Canvas(self.frame,bg='#FFFFFF',width=300,height=300)
        hbar=Scrollbar(self.frame,orient=HORIZONTAL)
        hbar.pack(side=BOTTOM,fill=X)
        hbar.config(command=self.canvas.xview)
        vbar=Scrollbar(self.frame,orient=VERTICAL)
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
        
        # start = time.time()
        test_label = Label()
        # print("Time to create test label: " + str(time.time() - start))

        start = time.time()
        #maths
        for column_counter in range(len(self.columns)):
            widths = [self.header.get_text_width(column_counter, test_label)]
            for record in self.records:
                widths.append(record.get_text_width(column_counter, test_label))
            self.column_widths.append(max(widths))
        record_width = sum(self.column_widths)
        print("Time to calculate widths: " + str(time.time() - start))

        larget_row_text = Label(text=str(len(self.records)))
        row_number_width = larget_row_text.winfo_reqwidth()
        larget_row_text.destroy()
        
        header_height = self.header.get_height(test_label)
        
        self.canvas.create_rectangle(2, 2, record_width + row_number_width, (header_height + (header_height * len(self.records))) - 2, fill=self.header.fill_color, outline="black", width=1)

        self.canvas.config(width=record_width + row_number_width, height=header_height + (header_height * len(self.records)), scrollregion=(2, 2, record_width + row_number_width, (header_height + (header_height * len(self.records)))))

        # draw row number background
        self.canvas.create_rectangle(3, header_height, row_number_width, header_height + (header_height * len(self.records)) - 2, fill='light grey', width=0)

        #draw row numbers
        for row_counter in range(len(self.records)):
            self.canvas.create_text((row_number_width/2), header_height + (row_counter * self.records[row_counter].get_height(test_label)) + (self.records[row_counter].get_height(test_label)/2), text=str(row_counter + 1), anchor='center')
        
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

        test_label.destroy()

    def reset(self):
        self.canvas.delete('all')
        self.records = []
        self.column_widths = []

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
