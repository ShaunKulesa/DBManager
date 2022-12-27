from tkinter import *
from tkinter import ttk
import tkinter as tk

root = Tk()
root.title("TestClass")
root.geometry("700x700")
root.resizable(False, False)

class TestClass:
    def __init__(self, master):
        # content = tk.Frame(root, bg = "#333333")
        #footer = tk.Frame(root, bg = "#333333", height = 60)

        # content.pack(fill = "both", expand = True)
        # footer.pack(fill = "both", side = "bottom")

        leftFrame = tk.Frame(root, bg = "#333333")
        leftFrame.grid(row = 0, column = 0, sticky = "nsew")

        middleFrame  = tk.Frame(root, bg = "#333333")
        middleFrame.grid(row = 0, column = 1, sticky = "nsew")

        rightFrame = tk.Frame(root, bg = "#333333")
        rightFrame.grid(row = 0, column = 2, sticky = "nsew")

        self.bottomFrame = tk.Frame(root, bg = "#333333")
        self.bottomFrame.grid(row = 1, column = 0, columnspan = 3, sticky = "nsew")

        root.rowconfigure(0, weight = 10, uniform="root")
        root.rowconfigure(1, weight = 1, uniform="root")
        root.columnconfigure(0, weight = 1, uniform="root")
        root.columnconfigure(1, weight = 1, uniform="root")
        root.columnconfigure(2, weight = 1, uniform="root")

        ### LEFT FRAME
        labelFrame1 = LabelFrame(leftFrame, text = "Label Frame 1")
        labelFrame1.grid(row = 0, column = 0, sticky = "nsew")

        labelFrame2 = LabelFrame(leftFrame, text = "Label Frame 2")
        labelFrame2.grid(row = 1, column = 0, sticky = "nsew")

        labelFrame3 = LabelFrame(leftFrame, text = "Label Frame 3")
        labelFrame3.grid(row = 2, column = 0, sticky = "nsew")

        leftFrame.rowconfigure(0, weight = 1, uniform="leftFrame")
        leftFrame.rowconfigure(1, weight = 1, uniform="leftFrame")
        leftFrame.rowconfigure(2, weight = 2, uniform="leftFrame")
        leftFrame.columnconfigure(0, weight = 1, uniform="leftFrame")

        ### MIDDLE FRAME
        labelFrame4 = LabelFrame(middleFrame, text = "Label Frame 1")
        labelFrame4.grid(row = 0, column = 1, sticky = "nsew")

        labelFrame5 = LabelFrame(middleFrame, text = "Label Frame 2")
        labelFrame5.grid(row = 1, column = 1, sticky = "nsew")

        labelFrame6 = LabelFrame(middleFrame, text = "Label Frame 3")
        labelFrame6.grid(row = 2, column = 1, sticky = "nsew")

        ### RIGHT FRAME
        labelFrame7 = LabelFrame(rightFrame, text = "Label Frame 1")
        labelFrame7.grid(row = 0, column = 2, sticky = "nsew")

        labelFrame8 = LabelFrame(rightFrame, text = "Label Frame 2")
        labelFrame8.grid(row = 1, column = 2, sticky = "nsew")

        labelFrame9 = LabelFrame(rightFrame, text = "Label Frame 3")
        labelFrame9.grid(row = 2, column = 2, sticky = "nsew")

if __name__ == "__main__":
    e = TestClass(root)
    root.mainloop()