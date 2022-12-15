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

        self.top_pane = MainFrameTopPane(self, "red")
        self.top_pane.pack(side=TOP, fill=BOTH, expand=True)

class MainFrameTopPane(PanedWindow):
    def __init__(self, parent, background_color):
        PanedWindow.__init__(self, parent, bg=background_color)
        self.parent = parent

        self.left_pane = Frame(self, bg=background_color)
        self.left_pane.pack(side=LEFT, fill=BOTH, expand=True)

        self.right_pane = Frame(self, bg=background_color)
        self.right_pane.pack(side=RIGHT, fill=BOTH, expand=True)

        self.add(self.left_pane)
        self.add(self.right_pane)

        openfile_button = Button(self, text="Open File")
        openfile_button.pack()
        
window = Window(ManinFrame, 800, 600, None)
mainloop()