from typing import Text
from tools.currency_manager import Converter
import tkinter as tkr

def Take_input():
    INPUT = tkr.inputtxt.get("1.0", "end-1c")
    print(INPUT)
    if(INPUT == "120"):
        tkr.Output.insert(tkr.END, 'Correct')
    else:
        tkr.Output.insert(tkr.END, "Wrong answer")

class Window:
    master = None
    converter = None

    def __init__(self):
        self.master = tkr.Tk()
        self.master.geometry("800x600")
        self.master.title("BRD Exchange")
        self.converter = Converter

    

    def show_window(self):
        self.master.mainloop()