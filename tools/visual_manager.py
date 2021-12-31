from typing import Text
from tools.currency_manager import Converter
import tkinter as tkr

class Window:
    master = None
    converter = None
    components = []

    def __init__(self):
        self.master = tkr.Tk()
        self.master.geometry("800x600")
        self.master.title("BRD Exchange")
        self.converter = Converter()
        self.components.append( tkr.Label(text="") )
        self.components.append( tkr.Text(self.master, height=1, width=25, bg='light cyan') )

    def text_edited(self, e):
        self.components[0].config( text=self.components[1].get(1.0,tkr.END) )
        pass

    def set_contents(self):

        self.components[1].bind('<KeyRelease>', self.text_edited)

        self.components[0].grid(row=1,column=0)
        self.components[1].grid(row=0,column=0)
        return self

    def show_window(self):
        self.master.mainloop()