from table import Table, Header, Record
from database_backend import SqliteHandler
from tkinter import *

class Window(Tk):
    def __init__(self, frame, *args):
        Tk.__init__(self)
        self.title("DBManager")
        self.geometry("800x600")

        self.frame = frame(self, *args)
        self.frame.pack()
    
    def switch_frame(self, frame, *args):
        self.frame.destroy()
        self.frame = frame(self, args)
        self.frame.pack()

class ManinFrame(Frame):
    def __init__(self, window, width, height, background_color):
        Frame.__init__(self, window, width=width, height=height, bg=background_color)
        self.window = window
        self.width = width
        self.height = height
        
window = Window(ManinFrame, 800, 600, None)
mainloop()