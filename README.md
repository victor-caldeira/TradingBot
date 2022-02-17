# TradingBot
 
> The bot implements the Momentum Strategy and consumes the [Binance API](https://github.com/binance/binance-spot-api-docs) for trading cryptocurrencies. The [BotFather API](https://github.com/AlexeySemigradsky/botfather) is used to send log information to user via a Telegram chatbot.

## Requirements
* First of all, be sure about what you're doing. Do your research, understand the risks and FIND THE BEST CONFIGURATION FOR YOU! The [Time-series-momentum](https://github.com/victor-caldeira/Time-series-momentum) may be a good tool when looking for the best configuration for your bot.
* Generate and enable an API key in your Binance account.
* Create a telegram chatbot with botfather.

## Bot details
* The bot trades one asset pair (ex: ETHUSDT or BTCUSDT) following the user configuration.
* By default (this is hard coded, but may be easily changed in a fork or next release):
   - The market data have a daily interval (24h);
   - Short sell is not allowed. The bot state may be long or neutral, but never short;
   - Logs are sent to telegram (except caught Exceptions).

## Setting up the bot
The bot configuration is made by using environment variables. So, before running it, you must create the following environment variables:
* api_key -> Binance API key
* api_secret -> Binance API secret
* bot_token -> Telegram chatbot token
* chat_id -> Telegram chat id
* asset -> asset pair (ex: ETHUSDT or BTCUSDT)
* first_trade_value -> First buy value (in USDT, BTC or no matter what currency traded). The next trades value will be the value of the preceding sell. 
* window -> window (in days) took into account in the momentum strategy
* trigger -> trigger to buy or sell
* trade_delay -> minimum delay between 2 trades (in seconds). Remember that you're using a daily interval on your data. It makes no sense trading each 10 seconds. Something between 30 minutes and 4 hours should be enougth.

## Disclaimer
Before using any strategy, do your own research. Losses are part of trading.

This project does not constitute any offer, recommendation or solicitation to any person to enter into any transaction or adopt any hedging, trading or investment strategy, nor does it constitute any prediction of likely future movement in rates or prices or any representation that any such future movements will not exceed those shown in any illustration.

This project is not an investment advice. I accept no liability and will not be liable for any loss or damage arising directly or indirectly (including special, incidental or consequential loss or damage) from your use of this project, howsoever arising, and including any loss, damage or expense arising from, but not limited to, any defect, error, imperfection, fault, mistake or inaccuracy with this project.
