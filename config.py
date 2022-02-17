import os

# API key and secret
api_key = os.environ.get('api_key')
api_secret = os.environ.get('api_secret')

# Telegram chat bot token
BOT_TOKEN = os.environ.get('bot_token')
CHAT_ID = os.environ.get('chat_id')

# Strategy config
asset = os.environ.get('asset') #'ETHUSDT'
first_trade_value = os.environ.get('first_trade_value') # 12 #USDT
window = os.environ.get('window') #11
trigger = os.environ.get('trigger') #0.005
trade_delay = os.environ.get('trade_delay') #7200 # minimum delay in seconds between 2 trades