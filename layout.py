from tkinter import *

root = Tk()
root.title("DBManager")
root.geometry("800x600")

root.update()

top_frame = Frame(width=root.winfo_width(), height=root.winfo_height() * 0.05, bg="red")
# top_frame.pack_propagate(0)
top_frame.grid(row=0, column=0, columnspan=2, sticky="nsew")

left_frame = Frame(width=root.winfo_width() * 0.20, height=root.winfo_height() * 0.95, bg="yellow", highlightbackground="black", highlightthickness=1)
# left_frame.pack_propagate(0)
left_frame.grid(row=1, column=0, sticky="nsew")

right_frame = Frame(width=root.winfo_width() * 0.80, height=root.winfo_height() * 0.95, bg="blue", highlightbackground="black", highlightthickness=1)
# right_frame.pack_propagate(0)
right_frame.grid(row=1, column=1, sticky="nsew")

root.mainloop()
