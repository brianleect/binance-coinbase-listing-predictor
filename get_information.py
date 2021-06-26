from bs4 import BeautifulSoup
from requests import get
from time import sleep
import pandas as pd
from ignore_list import ignore_list

def getTop1000(): # Top 1000
    
    try:
        tables = []

        # We first start by getting overall list of coins from coingecko?
        url = "https://www.coingecko.com/en?page="


        # In theory we could extract all 8000 coins by extending page to 81 update this accordingly works

        last_page=11 # Update this accordingly

        for page in range(1,last_page+1): # Gets top 1000 coins
            response = get(url+str(page)) # Query coingecko for table. Note that each page stores 100 symbols
            html_page = response.content
            table = BeautifulSoup(html_page, 'html.parser').find_all('table')
            df = pd.read_html(str(table))[0]
            tables.append(df)
            sleep(0.5)
            print("[Top 1000] Extracting page",page,"/",last_page)

        all_coins = pd.concat(tables)
        all_coins = all_coins.drop(columns=['Unnamed: 0','Last 7 Days']) # Remove unnecessary columns

        top_1000 = all_coins[0:1000]

        coins = []
        symbols = []
        # Add symbol column and edit coin column
        for index, row in top_1000.iterrows():
            try:
                split_word = row['Coin'].split()
                symbol = split_word[-1] # Gets symbol

                name = " ".join([word for word in split_word if word != symbol]) # Removes symbol from name and joins string
                if name == "": name = symbol # For edge cases like XRP XRP XRP
                coins.append(name)
                symbols.append(symbol)
            except Exception as e:
                print("Error occured:",e)
            #print("Count:",i)

        top_1000['Coin'] = coins # Replaces coin column with cleaned name # We take top 2800 due to '#' not being labelled after
        top_1000.insert(top_1000.columns.get_loc('Coin'), 'Symbol', symbols) # Insert symbol column after coin
        top_1000 = top_1000.query('Symbol not in @ignore_list')

        return top_1000
    except Exception as e:
        print("Error:",e)
        print("Getting top 1000 symbols failed")
        return 0

def getBinanceSymbols():
    try:
        url = "https://api.binance.com/api/v3/exchangeInfo" # Gets all exchange info from binance
        response = get(url).json()

        binance_symbols = []

        def isLevToken(symbol):
            if symbol[-2:] == 'UP': return True
            elif len(symbol) >= 6 and symbol[-4:] == 'DOWN': return True
            elif 'BULL' in symbol or 'BEAR' in symbol: return True
            else: return False

        # We filter for lev tokens
        for i in range(0,len(response['symbols'])):
            symbol = response['symbols'][i]['baseAsset']
            if (symbol not in binance_symbols) and (not isLevToken(symbol)): binance_symbols.append(symbol)

        print("Binance has a total of",len(binance_symbols),"unique crypto offerings")

        return binance_symbols
    except Exception as e:
        print("Error",e)
        print("Getting Binance Symbols failed")
        return 0

def getCoinbaseSymbols():
    try:
        url = 'https://api.pro.coinbase.com/products' # Hits CB REST API for all products
        response = get(url).json()

        coinbase_symbols = []

        for i in range(0,len(response)):
            symbol = response[i]['base_currency']
            if symbol not in coinbase_symbols: coinbase_symbols.append(symbol)
                
        print("Coinbase has a total of",len(coinbase_symbols),"unique symbols")

        return coinbase_symbols
    except Exception as e:
        print("Error",e)
        print("Getting Coinbase Symbols failed")
        return 0


def getCoinbaseCustodySymbols():
    try:
        url = 'https://api.custody.coinbase.com/api/marketing/currencies'
        response = get(url).json() 
        response

        print("No. of Coinbase Custody Symbols:",len(response))
        symbols = []
        for asset in response:
            symbols.append(asset['symbol'].upper())
        
        return symbols
    except Exception as e:
        print("Error",e)
        print("Getting Coinbase Custody Symbols failed")
        return 0
        


    