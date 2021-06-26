from time import sleep
import pandas as pd
from get_information import getTop1000, getBinanceSymbols, getCoinbaseSymbols, getCoinbaseCustodySymbols
import datetime

top_1000 = getTop1000()
binance_symbols = getBinanceSymbols()
coinbase_symbols = getCoinbaseSymbols()
cbc_symbols = getCoinbaseCustodySymbols()
last_updated = datetime.datetime.now()


def predictCoinbase():
    in_binance_not_coinbase = [symbol for symbol in binance_symbols if symbol not in coinbase_symbols]
    print("We have",len(in_binance_not_coinbase),"tokens in binance but NOT IN coinbase")

    df_ibncb = top_1000.query('Symbol in @in_binance_not_coinbase') # Finds symbols in binance but not coinbase
    view_num = int(input("How many symbols do you wish to view? "))
    filtered = df_ibncb[0:view_num]
    
    print(filtered)
    print('-----')
    top_1000_not_cb = top_1000.query('Symbol not in @coinbase_symbols') # Top 1000 filter against CB symbols
    print("We have",len(top_1000_not_cb),"tokens in top 1000 but NOT IN coinbase")
    view_num = int(input("How many symbols do you wish to view? "))
    filtered = top_1000_not_cb[0:view_num]
    print(filtered)

    print('--------')
    in_cbc_not_cb = [symbol for symbol in cbc_symbols if symbol not in coinbase_symbols] # In CB custody but not CB
    print("We have",len(in_cbc_not_cb),"symbols in CB Custody but not CB")
    df_cbc_cb = top_1000.query('Symbol in @in_cbc_not_cb')
    view_num = int(input("How many symbols do you wish to view? "))
    filtered = df_cbc_cb[0:view_num]
    print(filtered)

    return


    # Add in CB custody but not in CB!! (Quite impt?)
    # Need to figure scraping javascript site

    return 

def predictBinance():
    in_coinbase_not_binance = [symbol for symbol in coinbase_symbols if symbol not in binance_symbols]
    print("We have",len(in_coinbase_not_binance),"tokens in coinbase but NOT IN binance")

    df_icbnb = top_1000.query('Symbol in @in_coinbase_not_binance')
    print(df_icbnb)
    print('-------')
    top_1000_not_binance = top_1000.query('Symbol not in @binance_symbols') # Usage of query to get non-listed symbols
    print("We have",len(top_1000_not_binance),"tokens in top 1000 but NOT IN binance")

    view_num = int(input("How many symbols do you wish to view? "))
    filtered = top_1000_not_binance[0:view_num]
    print(filtered)

    return

def updateAll():
    global top_1000
    global binance_symbols
    global coinbase_symbols
    global last_updated
    
    top_1000 = getTop1000()
    binance_symbols = getBinanceSymbols()
    coinbase_symbols = getCoinbaseSymbols()
    last_updated = datetime.datetime.now()
    print("Successfully updated all")
    return

while True:
    action = input('Display what variable? \n 1: Top 1000\n 2: Binance Symbols \n 3: CB Symbols \n 4: Binance predictions \n 5: CB Predictions\n 6: Exit Program\n')
    if action =='1': print(top_1000)
    elif action == '2': print(binance_symbols)
    elif action == '3': print(coinbase_symbols)
    elif action == '4': predictBinance()
    elif action == '5': predictCoinbase()
    else: break