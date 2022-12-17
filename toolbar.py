from tkinter import *
from tkinter import ttk

class Toolbar(Frame):
    def __init__(self, parent, width, height):
        Frame.__init__(self, parent, width=width, height=height, background='#922724')
        self.parent = parent
        style = ttk.Style()
        style.theme_use('clam')
        style.configure('Toolbar.TFrame', background='#922724')

        style.configure('ToolbarButton.TButton', background='#922724', foreground='white', borderwidth=0, bg="#922724", relief = "flat", visible=False)
        style.map('ToolbarButton.TButton', background = [("pressed", "white"), ("active", "white")], foreground = [('pressed', 'black'), ('active', 'black')])
        style.map('ToolbarButton.TFrame', background = [("pressed", "white"), ("active", "white"), ("focus", "white")], foreground = [('pressed', 'black'), ('active', 'black')])

class ToolbarButton(ttk.Button):
    def __init__(self, window, parent, text):
        ttk.Button.__init__(self, parent, text=text, style='ToolbarButton.TButton', takefocus=False, command=self.on_click)

        self.update()
        self.popup_frame = ttk.Frame(window, style='ToolbarButton.TFrame')

        self.popup_frame.bind('<Leave>', self.on_leave)
    
    def on_click(self):
        self.popup_frame.place(x=self.winfo_x(), y=self.winfo_y() + self.winfo_height())
        self.popup_frame.tkraise()
    
    def on_leave(self, event):
        self.popup_frame.place_forget()
        
    def add_button(self, text):
        button = ttk.Button(self.popup_frame, text=text, style='ToolbarButton.TButton', takefocus=False)
        button.pack(fill=Y)


# window = Tk()
# frame = Frame(window)
# toolbar = Toolbar(frame, 500, 25)

# button = ToolbarButton(window, toolbar, text="File")
# button.pack(side=LEFT, fill=Y)
# button.add_button('New')

# button = ToolbarButton(window, toolbar, text="Edit")
# button.pack(side=LEFT, fill=Y)
# button.add_button('Copy')

# toolbar.pack(side=TOP, fill=X)
# frame.pack(side=TOP, fill=BOTH, expand=True)
# mainloop()