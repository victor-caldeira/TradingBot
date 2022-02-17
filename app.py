from binance import Client
import pandas as pd
import numpy as np
import datetime
import time

import config
from logService import error_message_and_delay, print_and_send, print_to_txt

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
        
    print_and_send(f'{datetime.datetime.now()}, {df.Close[-1]}, {momentum}, {balance}, {long}, {trade}', log_file, BOT_TOKEN, CHAT_ID)

    return value_to_trade #balance 



# Initialize
value_to_trade = float(config.first_trade_value)
BOT_TOKEN = config.BOT_TOKEN
CHAT_ID = config.CHAT_ID
date_time = datetime.datetime.now()
log_file = str("log_" + date_time.strftime("%m-%d-%Y_%H%M%S") + ".txt")

while True:
    try:
        client = Client(config.api_key, config.api_secret)
        break
    except Exception as e:
        error_message_and_delay(e, log_file, 300)

while True:
    try:
        print_and_send('----------------------------------------------------', log_file, BOT_TOKEN, CHAT_ID)
        print_and_send(f'Start running at {date_time}. Asset: {config.asset} . First trade value: {value_to_trade} USDT', log_file, BOT_TOKEN, CHAT_ID)
        print_and_send(f'Config -> Window: {config.window} days. Trigger: {config.trigger}. Trade delay: {config.trade_delay}', log_file, BOT_TOKEN, CHAT_ID)
        print_and_send('', log_file, BOT_TOKEN, CHAT_ID)
        print_and_send(f'Time, Price, Momentum, Balance, Long, Trade', log_file, BOT_TOKEN, CHAT_ID)
        break

    except Exception as e:
        error_message_and_delay(e, log_file, 1800)

run = True

while run:

    while True:
       try:
            open_orders = client.get_open_orders(symbol=config.asset)
            if len(open_orders) > 0:
                client._delete('openOrders', True, data={'symbol': config.asset}) # Delete all open orders (if last order was not executed)

            balance = client.get_asset_balance(asset=config.asset[:3])['free']

            break

       except Exception as e:
            error_message_and_delay(e, log_file, 1800)

    balance = float(balance)

    if balance>=0.0001: #Change it to run with different assets
        long = True
    elif balance<0:
        while True:
            try:
                print_and_send("Warning! Asset balance < 0", log_file, BOT_TOKEN, CHAT_ID)
                break
            except Exception as e:
                error_message_and_delay(e, log_file, 300)

        run = False
    else:
        long = False

    while True:
       try:
           df = get_data(config.asset, '1d', str( int(config.window) + 1)+' day')
           value_to_trade = trade_strategy(df, float(config.trigger), long, value_to_trade) # When really running, don't return balance
           break
       except Exception as e:
            error_message_and_delay(e, log_file, 1800)



    time.sleep( int(config.trade_delay) ) #delay in seconds
    
