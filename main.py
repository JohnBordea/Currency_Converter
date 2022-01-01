"""import tkinter as tk
from tkinter import ttk
  
# Creating tkinter window
window = tk.Tk()
window.geometry('350x250')
# Label
ttk.Label(window, text = "Select the Month :", 
        font = ("Times New Roman", 10)).grid(column = 0, 
        row = 15, padx = 10, pady = 25)
  
n = tk.StringVar()
monthchoosen = ttk.Combobox(window, width = 27, state="readonly",
                            textvariable = n)
  
# Adding combobox drop down list
monthchoosen['values'] = (' January', 
                          ' February',
                          ' March',
                          ' April',
                          ' May',
                          ' June', 
                          ' July', 
                          ' August', 
                          ' September', 
                          ' October', 
                          ' November', 
                          ' December')

monthchoosen.grid(column = 1, row = 15)

def modified (event) :
    print(monthchoosen.get())

monthchoosen.bind('<<ComboboxSelected>>', modified)
# Shows february as a default value
monthchoosen.current(0) 
window.mainloop()"""

from tools.visual_manager import Window

window = Window()
window.set_contents()
window.show_window()

