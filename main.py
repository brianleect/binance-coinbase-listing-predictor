from time import sleep
import pandas as pd
from get_information import getTop1000, getBinanceSymbols, getCoinbaseSymbols, getCoinbaseCustodySymbols
import datetime
import time
from params import SEND_TELE ,VIEW_NUM, token, chat_id, SEND_TELEGRAM_FAIL_INTERVAL, SEND_INTERVAL
import telegram as telegram
from tabulate import tabulate
from helper_functions import durationToSeconds

try:
    bot = telegram.Bot(token=token)
except Exception as e:
    print("Error initializing telegram bot")
    print(e)
    quit()

def send_message(message):
    while True:
        try:
            bot.send_message(chat_id=chat_id,text=message)
            break
        except Exception as e:
            print("Error:",e)
            print("Retrying to send tele message in",SEND_TELEGRAM_FAIL_INTERVAL,"s")
            sleep(SEND_TELEGRAM_FAIL_INTERVAL)

def predictCoinbase():
    
    msg1 = ''
    in_cbc_not_cb = [symbol for symbol in cbc_symbols if symbol not in coinbase_symbols] # In CB custody but not CB
    df_cbc_cb = top_1000.query('Symbol in @in_cbc_not_cb')
    filtered = df_cbc_cb[0:VIEW_NUM].drop(columns=['Coin','24h Volume','Mkt Cap'])
    msg1 += "We have "+str(len(in_cbc_not_cb))+" symbols in CB Custody but not CB\n\n"
    msg1 += tabulate(filtered,tablefmt="pipe", headers="keys", showindex=False) + '\n ---------------------------------------------------------------------------------\n\n'
    
    msg2 = ''
    in_binance_not_coinbase = [symbol for symbol in binance_symbols if symbol not in coinbase_symbols]
    df_ibncb = top_1000.query('Symbol in @in_binance_not_coinbase') # Finds symbols in binance but not coinbase
    filtered = df_ibncb[0:VIEW_NUM].drop(columns=['Coin','24h Volume','Mkt Cap'])
    msg2 += "We have "+str(len(in_binance_not_coinbase))+" tokens in binance but NOT IN coinbase\n\n"
    msg2 += tabulate(filtered,tablefmt="pipe", headers="keys", showindex=False) + '\n ---------------------------------------------------------------------------------\n\n'
    
    msg3 = ''
    top_1000_not_cb = top_1000.query('Symbol not in @coinbase_symbols') # Top 1000 filter against CB symbols
    filtered = top_1000_not_cb[0:VIEW_NUM].drop(columns=['Coin','24h Volume','Mkt Cap'])
    msg3 += "We have "+str(len(top_1000_not_cb))+" tokens in top 1000 but NOT IN coinbase\n\n"
    msg3 += tabulate(filtered,tablefmt="pipe", headers="keys", showindex=False) + '\n ---------------------------------------------------------------------------------\n\n'

    if SEND_TELE:
        send_message(msg1)
        send_message(msg2)
        send_message(msg3)
    else:
        print(msg1,'\n',msg2,'\n',msg3)

    return

def predictBinance():
    msg = ''
    in_coinbase_not_binance = [symbol for symbol in coinbase_symbols if symbol not in binance_symbols]
    df_icbnb = top_1000.query('Symbol in @in_coinbase_not_binance').drop(columns=['Coin','24h Volume','Mkt Cap'])
    msg += "We have "+str(len(in_coinbase_not_binance))+" tokens in coinbase but NOT IN binance\n\n"
    msg+= tabulate(df_icbnb,tablefmt="pipe", headers="keys", showindex=False) + '\n ---------------------------------------------------------------------------------\n\n'

    top_1000_not_binance = top_1000.query('Symbol not in @binance_symbols') # Usage of query to get non-listed symbols
    filtered = top_1000_not_binance[0:VIEW_NUM].drop(columns=['Coin','24h Volume','Mkt Cap'])
    msg += "We have "+str(len(top_1000_not_binance))+" tokens in top 1000 but NOT IN binance\n\n"
    msg += tabulate(filtered,tablefmt="pipe", headers="keys", showindex=False) + '\n ---------------------------------------------------------------------------------\n\n'

    if SEND_TELE: send_message(msg)
    else: print(msg)

    return

def updateAll():
    global top_1000
    global binance_symbols
    global coinbase_symbols
    global cbc_symbols
    global start_extract
    global last_updated
    global extract_time
    
    start_extract = time.time()
    top_1000 = getTop1000()
    binance_symbols = getBinanceSymbols()
    coinbase_symbols = getCoinbaseSymbols()
    cbc_symbols = getCoinbaseCustodySymbols()
    last_updated = time.time()
    print("Successfully updated all")
    return


top_1000 = binance_symbols = coinbase_symbols = cbc_symbols = last_updated = extract_time = start_extract = 0 # Initialize relevant variables

# Initial send
updateAll()
predictCoinbase()
predictBinance()

SEND_INTERVAL = durationToSeconds(SEND_INTERVAL) # Convert string to seconds for sleep usage
init_dt = datetime.datetime.now() # Used to determine total time program ran

if SEND_TELE:
    while True:
        print("Extract time:",last_updated-start_extract,'/ Time ran:',datetime.datetime.now()-init_dt)
        while time.time() - last_updated < SEND_INTERVAL:
            print("Sleeping for:",SEND_INTERVAL-time.time()+last_updated,'seconds')
            sleep(SEND_INTERVAL-time.time()+last_updated) # Sleeps for the remainder of 1s
            pass # Loop until 1s has passed to getPrices again
        
        updateAll()
        predictCoinbase()
        predictBinance()