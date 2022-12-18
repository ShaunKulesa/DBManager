import time
import tkinter.font as tkfont
from tkinter import *

window = Tk()

test_label = Label(window, text="test", font=("Consolas", 10))



start = time.time()
font = tkfont.Font(family="Consolas", size=10, weight="normal")
print((time.time() - start) * 1000)

start = time.time()
test_label.config(text="test")
print((time.time() - start) * 1000)

start = time.time()
for i in range(1000):
    font.measure("test")
print((time.time() - start) * 1000)

start = time.time()
for i in range(1000):
    test_label.winfo_reqwidth()
print((time.time() - start) * 1000)

window.mainloop()