from tkinter import *
import time


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
        self.canvas = Canvas()
        self.canvas.pack(anchor='center')
        self.table_name = table_name

        self.column_widths = []
    
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

        header_height = self.header.get_height()

        self.canvas.create_rectangle(0, 0, record_width, header_height + (30 * len(self.records)), fill=self.header.fill_color, outline=self.header.outline_color, width=self.header.outline_width)

        previous_column_width = -3

        self.canvas.config(width=record_width, height=header_height + (header_height * len(self.records)))

        self.canvas.create_line(3, header_height, record_width, header_height, fill=self.header.outline_color, width=self.header.outline_width)
        for i in range(len(self.columns)):
            previous_column_width += (self.column_widths[i])
            self.canvas.create_text(previous_column_width, header_height / 2, text=self.columns[i], anchor='e')
            self.canvas.create_line(previous_column_width + 3, 0, previous_column_width + 3, header_height + (30 * len(self.records)), fill='#D3D3D3', width=self.header.outline_width)
        
        #create record text
        for record_counter in range(len(self.records)):
            previous_column_width = -3
            #create record
            self.canvas.create_line(0, (header_height * (record_counter + 1)), record_width, (header_height * (record_counter + 1)), fill="#D3D3D3", width=self.header.outline_width)
            for column_counter in range(len(self.columns)):
                previous_column_width += (self.column_widths[column_counter])
                self.canvas.create_text(previous_column_width - (self.column_widths[column_counter] / 2), (header_height * (record_counter + 1)) + (header_height / 2), text=self.records[record_counter].data[column_counter], anchor='center')
root = Tk()

table = Table('Person')
header = Header(table, ['firstName', 'lastName', 'Age'])
table.add_header(header)
table.add_records([Record(table, ['Shaun', 'Kulesa', 17,])] * 10)
table.add_records([Record(table, ['John', 'Doe', 20,])] * 10)

table.draw()


        
finish = time.perf_counter()
print(f'Finished in {round(finish-start, 2)} second(s)')

mainloop()
