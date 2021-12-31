from typing import Text
from tools.currency_manager import Converter
import tkinter as tkr

class Window:
    master = None
    converter = None
    components = []
    interaction_at = None

    def __init__(self):
        self.master = tkr.Tk()
        self.master.geometry("800x600")
        self.master.title("BRD Exchange")
        self.converter = Converter()
        self.components.append( tkr.Text(self.master, height=1, width=25, bg='light cyan', bd=0) )
        self.components.append( tkr.Text(self.master, height=1, width=25, bg='light cyan', bd=0) )
        f = tkr.Text(self.master, height=1, width=25, bg='light cyan')
        #f.delete()
        #self.components.append( tkr.Label(text="") )

    def text_edited(self, event, index_from, index_to):
        self.components[index_to].delete(1.0, 'end')
        self.components[index_to].insert(1.0, self.components[index_from].get(1.0,tkr.END))
        if index_from != self.interaction_at:
            self.interaction_at = 0
        #print(self.components[0])

    def set_contents(self):

        self.components[0].bind( '<KeyRelease>', lambda event: self.text_edited_upper(event, 0, 1) )

        self.components[0].grid(row=0,column=0)
        self.components[1].grid(row=1,column=0)
        return self

    def show_window(self):
        self.master.mainloop()