from tools.visual_manager import Window
from tools.currency_manager import Converter

window = Window()
window.set_contents()
window.show_window()

c = Converter()
print(c.exchange_rate)
print(c.curency_name)

print( list(c.curency_name.values()).index(c.to_currency) )