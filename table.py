from tkinter import *            

class Header:
    def __init__(self, table, data=[], outline_color='black', fill_color='white', outline_width=0):
        self.table = table
        self.table_name = table.table_name
        self.data = data
        self.outline_color = outline_color
        self.fill_color = fill_color
        self.outline_width = outline_width

        # self.height = 30
    
    def get_name(self):
        return self.table_name
    
    def get_columns(self):
        return self.data
    
    def get_text_width(self, column):
        text = Label(text=self.data[column])
        print(self.data[column])
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
        self.canvas.pack(anchor='n', fill='both', expand=True)
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
            print(widths)
            for record in self.records:
                widths.append(record.get_text_width(column_counter))
            self.column_widths.append(max(widths))
        record_width = sum(self.column_widths)

        # #draw
        # self.canvas.config(width=record_width, height=self.header.get_height() + (self.header.get_height() * len(self.records)))
        self.canvas.create_rectangle(0, 0, record_width, self.header.get_height(), fill=self.header.fill_color, outline=self.header.outline_color, width=self.header.outline_width)

        previous_column_width = -5
        for i in range(len(self.columns)):
            previous_column_width += (self.column_widths[i])
            self.canvas.create_text(previous_column_width, self.header.get_height() / 2, text=self.columns[i], anchor='e')

root = Tk()

table = Table('Person')
header = Header(table, ['firstName', 'lastName', 'Age'])
table.add_header(header)
# table.add_records([Record(table, ['Shaun', 'Kulesa', 17,])] * 10000)
table.draw()

mainloop()
