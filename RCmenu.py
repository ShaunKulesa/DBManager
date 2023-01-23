import tkinter as tk

class Smart_menu(tk.Menu):
    """A subclass of menu that opens when do_popup
    is triggered at the event position"""
    def __init__(self, *args, bindevent='<3>', **kwargs):
        super().__init__(*args, **kwargs)
        args[0].bind(bindevent, self.do_popup)

    def do_popup(self, event):
        try:
            self.tk_popup(event.x_root, event.y_root)
        finally:
            self.grab_release()


root = tk.Tk()
m = Smart_menu(root)
print(m)
m.add_command(label='test')
root.mainloop()
