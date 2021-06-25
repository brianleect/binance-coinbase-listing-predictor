from time import sleep
import pandas as pd
from get_information import getTop1000, getBinanceSymbols, getCoinbaseSymbols

top_1000 = getTop1000()
binance_symbols = getBinanceSymbols()
cb_symbols = getCoinbaseSymbols()

while True:
    action = input('Display what variable? ')
    if action =='1': print(top_1000)
    elif action == '2': print(binance_symbols)
    elif action == '3': print(cb_symbols)
    else: break