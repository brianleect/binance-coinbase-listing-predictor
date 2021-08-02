# listing-predictor
Attempts to predict possible future listings for binance and coinbase based on data from top 1000 coins.

Telegram Demo: https://t.me/coinbase_binance_predict_listing

![image](https://user-images.githubusercontent.com/63389110/127801749-bf2957d5-7a72-44af-a2a0-81a1524de40c.png)


## Usage

1. In command line run ```pip install -r requirements.txt```
2. Run "main.py" with command ```python main.py```
3. Follow instructions for options in command line.

Note: For display of symbols if it's too large it will not be fully visible. Try to view <50 symbols if possible.

## Extraction sources
1. Coingecko (Top 1000 data)
2. Binance API (Symbol information)
3. Coinbase API (Symbol information)
4. Coinbase Custody API (Symbol information)

## Implementations / Todos
~~1. Implement telegram bot interaction~~
~~2. Implement pandas dataframe display capability~~
~~3. Customizable interval implementation (Host on VPS)~~

