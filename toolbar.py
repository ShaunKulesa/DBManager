from tkinter import *
from tkinter import ttk

class Toolbar(ttk.Frame):
    def __init__(self, parent, width, height):
        ttk.Frame.__init__(self, parent, width=width, height=height, style='Toolbar.TFrame')
        self.parent = parent

        self.update()

        style = ttk.Style()
        style.theme_use('clam')
        style.configure('Toolbar.TFrame', background='#922724')

        style.configure('ToolbarButton.TButton', background='#922724', foreground='white', borderwidth=0, bg="#922724", relief = "flat", visible=False)
        style.map('ToolbarButton.TButton', background = [("pressed", "white"), ("active", "white")], foreground = [('pressed', 'black'), ('active', 'black')])
        style.map('ToolbarButton.TFrame', background = [("pressed", "white"), ("active", "white"), ("focus", "white")], foreground = [('pressed', 'black'), ('active', 'black')])

class ToolbarButton(ttk.Button):
    def __init__(self, parent, text):
        ttk.Button.__init__(self, parent, text=text, style='ToolbarButton.TButton', takefocus=False)

        self.update()
        self.popup_frame = ttk.Frame(parent.parent, style='ToolbarButton.TFrame')
        self.bind('<Enter>', self.on_enter)
        self.bind('<Leave>', self.on_leave)

        self.popup_frame.bind('<Enter>', self.on_enter)
        self.popup_frame.bind('<Leave>', self.on_leave)
    
    def on_enter(self, event):
        print(self.winfo_rootx(), self.winfo_rooty())
        self.popup_frame.place(x=self.winfo_rootx(), y=self.winfo_rooty())
    
    def on_leave(self, event):
        self.popup_frame.place_forget()
        
    def add_button(self, text):
        button = ttk.Button(self.popup_frame, text=text, style='ToolbarButton.TButton', takefocus=False)
        button.pack(side=LEFT, fill=Y)

# window = Tk()
# toolbar = Toolbar(window, 500, 25)

# button = ToolbarButton(toolbar, text="File")
# button.pack(side=LEFT, fill=Y)
# button.add_button('New')

# button = ToolbarButton(toolbar, text="Edit")
# button.pack(side=LEFT, fill=Y)
# button.add_button('Copy')

# toolbar.pack(side=TOP, fill=X)
# mainloop()