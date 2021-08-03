# listing-predictor
Attempts to predict possible future listings for binance and coinbase based on data from top 1000 coins.

Telegram Demo: https://t.me/coinbase_binance_predict_listing

![image](https://user-images.githubusercontent.com/63389110/127801749-bf2957d5-7a72-44af-a2a0-81a1524de40c.png)


## Usage

1. In command line run ```pip install -r requirements.txt```
2. Add telegram bot token + chat_id information to ```params.py```
3. Customize other params to personal preference (Read comments for details) (Note that default params work as well)
4. Run "main.py" with command ```python main.py```
5. You should either receive a tele message or have information printed to console


## Extraction sources
1. Coingecko (Top 1000 data)
2. Binance API (Symbol information)
3. Coinbase API (Symbol information)
4. Coinbase Custody API (Symbol information)

## Features
1. Telegram message
2. Pandas dataframe display capability (Tabulate)
3. Customizable message interval

## Todos
1. None atm
