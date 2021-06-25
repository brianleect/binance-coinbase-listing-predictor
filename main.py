from time import sleep
import pandas as pd
from get_information import getTop1000, getBinanceSymbols, getCoinbaseSymbols
import datetime

top_1000 = getTop1000()
binance_symbols = getBinanceSymbols()
coinbase_symbols = getCoinbaseSymbols()
last_updated = datetime.datetime.now()

def predictCoinbase():
    in_binance_not_coinbase = [symbol for symbol in binance_symbols if symbol not in coinbase_symbols]
    print("We have",len(in_binance_not_coinbase),"tokens in binance but NOT IN coinbase")

    df_ibncb = top_1000.query('Symbol in @in_binance_not_coinbase')
    print(df_ibncb)
    return df_ibncb[0:50]

def predictBinance():
    in_coinbase_not_binance = [symbol for symbol in coinbase_symbols if symbol not in binance_symbols]
    print("We have",len(in_coinbase_not_binance),"tokens in coinbase but NOT IN binance")

    df_icbnb = top_1000.query('Symbol in @in_coinbase_not_binance')
    print(df_icbnb)
    return df_icbnb

def updateAll():
    top_1000 = getTop1000()
    binance_symbols = getBinanceSymbols()
    cb_symbols = getCoinbaseSymbols()
    last_updated = datetime.datetime.now()
    return top_1000, binance_symbols, cb_symbols, last_updated

while True:
    action = input('Display what variable? ')
    if action =='1': print(top_1000)
    elif action == '2': print(binance_symbols)
    elif action == '3': print(coinbase_symbols)
    elif action == '4': predictBinance()
    elif action == '5': predictCoinbase()
    else: break