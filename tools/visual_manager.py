from typing import Text
from tools.currency_manager import Converter
import tkinter as tkr
from tkinter import ttk

class Window:
    master = None
    converter = None
    components = []

    can_be_typed = ('0', '1', '2', '3', '4', '5', '6', '7', '8', '9')

    interaction_at = 0
    changed_widget = False

    numbers_after_dot = 0

    def __init__(self):
        self.master = tkr.Tk()
        self.master.geometry("800x600")
        self.master.title("BRD Exchange")
        self.converter = Converter()

        self.components.append( tkr.Text(self.master, height=1, width=25, bg='#e9e9e9', bd=0) )
        self.components.append( tkr.Text(self.master, height=1, width=25, bg='#e9e9e9', bd=0) )

        self.components.append( ttk.Combobox(self.master, width = 27, state="readonly", textvariable = tkr.StringVar()) )
        self.components.append( ttk.Combobox(self.master, width = 27, state="readonly", textvariable = tkr.StringVar()) )

        self.components.append( tkr.Label(self.master, text='') )
        self.components.append( tkr.Label(self.master, text='') )
        self.components.append( tkr.Label(self.master, text='') )

        self.components[0].insert(1.0, self.converter.value_from)
        self.components[1].insert(1.0, self.converter.value_to)
        self.components[2]['values'] = list(self.converter.curency_name)
        self.components[2].current(0)
        self.components[3]['values'] = list(self.converter.curency_name)
        self.components[3].current(28)

    def text_widget_possible_length(self, st: str) -> int:
        if '.' in st:
            return 17
        return 12

    def text_edit(self, event, index_from, reverse=False):
        if event.keysym.lower() == 'escape':
            self.converter.value_from = 0
            self.converter.value_to = 0
            return "break"

        if index_from != self.interaction_at:
            self.interaction_at = index_from
            self.converter.value_from, self.converter.value_to = self.converter.value_to, self.converter.value_from
            self.changed_widget = True

        if self.changed_widget == True:
            if event.char in self.can_be_typed:
                self.converter.value_from = int(event.char)
                self.converter.exchange(reverse)
                self.changed_widget = False
            elif event.char == '.':
                self.converter.value_from = 0.0
                self.converter.exchange(reverse)
                self.changed_widget = False
            elif event.keysym.lower() == 'backspace':
                self.converter.value_from = 0
                self.converter.value_to = 0
                self.changed_widget = False
        else:
            if len( self.components[index_from].get(1.0,tkr.END) ) > self.text_widget_possible_length( self.components[index_from].get(1.0,tkr.END) ) or self.numbers_after_dot == 4:
                if event.char == '.':
                    self.converter.value_from = float(self.converter.value_from)
                    self.converter.exchange(reverse)
                elif event.keysym.lower() == 'backspace':
                    if '.' in self.components[index_from].get(1.0,tkr.END):
                        if self.numbers_after_dot == 0:
                            self.converter.value_from = int(self.converter.value_from)
                            self.converter.exchange(reverse)
                        else:
                            self.numbers_after_dot = self.numbers_after_dot - 1
                            self.converter.value_from = int(self.converter.value_from * (10 ** self.numbers_after_dot)) / (10 ** self.numbers_after_dot)
                            self.converter.exchange(reverse)
                    else:
                        self.converter.value_from = int((self.converter.value_from) / 10)
                        self.converter.exchange(reverse)

            elif event.char in self.can_be_typed:
                if '.' in self.components[index_from].get(1.0,tkr.END) and self.numbers_after_dot < 4:
                    self.numbers_after_dot = self.numbers_after_dot + 1
                    self.converter.value_from = round(self.converter.value_from + (int(event.char) / (10 ** self.numbers_after_dot)) , 4)
                    self.converter.exchange(reverse)
                else:
                    self.converter.value_from = self.converter.value_from * 10 + int(event.char)
                    self.converter.exchange(reverse)

            elif event.char == '.':
                self.converter.value_from = float(self.converter.value_from)
                self.converter.exchange(reverse)

            elif event.keysym.lower() == 'backspace':
                if '.' in self.components[index_from].get(1.0,tkr.END):
                    if self.numbers_after_dot == 0:
                        self.converter.value_from = int(self.converter.value_from)
                        self.converter.exchange(reverse)
                    else:
                        self.numbers_after_dot = self.numbers_after_dot - 1
                        self.converter.value_from = int(self.converter.value_from * (10 ** self.numbers_after_dot)) / (10 ** self.numbers_after_dot)
                        self.converter.exchange(reverse)
                else:
                    self.converter.value_from = int((self.converter.value_from) / 10)
                    self.converter.exchange(reverse)

        return "break"

    def text_show(self, event, index_from, index_to):
        self.components[index_from].delete(1.0, 'end')
        self.components[index_to].delete(1.0, 'end')
        self.components[index_from].insert(1.0, self.converter.value_from)
        self.components[index_from].configure(font = ("Times New Roman", 12, "bold"))
        self.components[index_to].insert(1.0, self.converter.value_to)
        self.components[index_to].configure(font = ("Times New Roman", 12, "normal"))

    def change_currency(self, event, index_from, index_to):

        if index_from == 0:
            self.converter.change_from( self.converter.curency_name[ self.components[2 + index_from].get() ] )
        else:
            self.converter.change_to( self.converter.curency_name[ self.components[2 + index_from].get() ] )

        self.converter.exchange(not self.interaction_at == 0)

        self.components[0].delete(1.0, 'end')
        self.components[1].delete(1.0, 'end')

        self.components[0 if self.interaction_at == 0 else 1].insert(1.0, self.converter.value_from)
        self.components[1 if self.interaction_at == 0 else 0].insert(1.0, self.converter.value_to)

        self.components[4].config(text=f"1 {self.converter.from_currency} - {self.converter.get_base_exchange_value()} {self.converter.to_currency}")
        self.components[5].config(text=f"1 {self.converter.to_currency} - {self.converter.get_base_exchange_value(True)} {self.converter.from_currency}")

    def set_contents(self):

        #Logic
        self.components[0].bind( '<Key>', lambda event: self.text_edit(event, 0) )
        self.components[1].bind( '<Key>', lambda event: self.text_edit(event, 1, True) )
        self.components[0].bind( '<KeyRelease>', lambda event: self.text_show(event, 0, 1) )
        self.components[1].bind( '<KeyRelease>', lambda event: self.text_show(event, 1, 0) )

        self.components[2].bind('<<ComboboxSelected>>', lambda event: self.change_currency(event, 0, 1) )
        self.components[3].bind('<<ComboboxSelected>>', lambda event: self.change_currency(event, 1, 0) )

        self.components[4].config(text=f"1 {self.converter.from_currency} - {self.converter.get_base_exchange_value()} {self.converter.to_currency}")
        self.components[5].config(text=f"1 {self.converter.to_currency} - {self.converter.get_base_exchange_value(True)} {self.converter.from_currency}")

        self.components[6].config(text="")

        #Style
        self.components[0].configure(font = ("Times New Roman", 12, "normal"))
        self.components[1].configure(font = ("Times New Roman", 12, "normal"))
        self.components[2].configure(font = ("Times New Roman", 12, "normal"))
        self.components[3].configure(font = ("Times New Roman", 12, "normal"))
        self.components[4].configure(font = ("Times New Roman", 12, "normal"))
        self.components[5].configure(font = ("Times New Roman", 12, "normal"))
        self.components[6].configure(font = ("Times New Roman", 12, "normal"))

        #Positioning
        self.components[0].grid(row=0, column=0, padx=(150, 10), pady=(75, 10))
        self.components[1].grid(row=1, column=0, padx=(150, 10))

        self.components[2].grid(row=0, column=1, pady=(75, 10))
        self.components[3].grid(row=1, column=1)

        self.components[4].grid(row=2, column=0, columnspan=2, padx=(150, 10))
        self.components[5].grid(row=3, column=0, columnspan=2, padx=(150, 10))

        self.components[6].grid(row=4, column=0, columnspan=2, padx=(150, 10))

    def show_window(self):
        self.master.mainloop()