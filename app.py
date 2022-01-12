from binance import Client
import pandas as pd
import numpy as np
import datetime
import time

import config
from print_to_txt import print_to_txt

def get_data(ticker, interval, window):
    df = pd.DataFrame(client.get_historical_klines(ticker, interval, window))
    df = df.iloc[:,:6]
    df.columns = ['Date', 'Open', 'High', 'Low', 'Close', 'Volume']
    df = df.set_index('Date')
    df.index = pd.to_datetime(df.index, unit='ms')
    df = df.astype(float)
    return df

def trade_strategy(df, trigger, long, value_to_trade):
    df = df.copy()
    df['log_ret'] = np.log(df.Close.pct_change() + 1)
    momentum = df.log_ret.sum()
    #df.dropna(inplace = True)

    if momentum<trigger and long:
        # Sell it
        qty = float(client.get_asset_balance(asset=config.asset[:3])['free']) * 0.999 // 0.0001 / 10000 # Round down
        value_to_trade = qty * float(df['Close'].tail(1))
        order = client.order_limit_sell(
            symbol=config.asset,
            quantity=qty,
            price=float(df['Close'].tail(1)))
        trade = (-1)

    elif momentum>=trigger and not long:
        # Buy it
        qty = value_to_trade/float(df['Close'].tail(1)) * 0.999 // 0.0001 / 10000 # Round down
        order = client.order_limit_buy(
            symbol=config.asset,
            quantity=qty,
            price=float(df['Close'].tail(1)))
        trade = 1

    else:
        trade = 0
        
    print_to_txt(f'{datetime.datetime.now()}, {df.Close[-1]}, {momentum}, {balance}, {long}, {trade}', 'log.txt', BOT_TOKEN, CHAT_ID)

    
    return value_to_trade #balance # When really running, don't need to return balance



# Initialize
client = Client(config.api_key, config.api_secret)
value_to_trade = config.first_trade_value
BOT_TOKEN = config.BOT_TOKEN
CHAT_ID = config.CHAT_ID

print_to_txt('----------------------------------------------------', 'log.txt', BOT_TOKEN, CHAT_ID)
print_to_txt(f'Start running at {datetime.datetime.now()}. Trading {value_to_trade} USDT', 'log.txt', BOT_TOKEN, CHAT_ID)
print_to_txt('', 'log.txt', BOT_TOKEN, CHAT_ID)
print_to_txt(f'Time, Price, Momentum, Balance, Long, Trade', 'log.txt', BOT_TOKEN, CHAT_ID)

run = True

 # DELETE WHEN REALLY RUNNING
'''
while True:
     try:
         balance = client.get_asset_balance(asset=config.asset[:3])['free']
         break
     except TypeError:
         print_to_txt("Error reading balance. Retrying...", 'log.txt')

balance = float(balance) # DELETE WHEN REALLY RUNNING
'''

while run:
    if len(client.get_open_orders(symbol=config.asset)) > 0:
        client._delete('openOrders', True, data={'symbol': config.asset}) # Delete all open orders (if last order was not executed)

    # Uncomment WHEN REALLY RUNNING
    while True:
       try:
            balance = client.get_asset_balance(asset=config.asset[:3])['free']
            break
       except ValueError:
            print_to_txt("Error reading balance. Retrying...", 'log.txt', BOT_TOKEN, CHAT_ID)
    balance = float(balance)

    if balance>=0.0001:
        long = True
    elif balance<0:
        print_to_txt("Warning! Asset balance < 0", 'log.txt', BOT_TOKEN, CHAT_ID)
        run = False
    else:
        long = False

    df = get_data(config.asset, '1d', str(config.window + 1)+' day')
    value_to_trade = trade_strategy(df, config.trigger, long, value_to_trade) # When really running, don't return balance

    time.sleep(config.trade_delay) #delay in seconds
    
