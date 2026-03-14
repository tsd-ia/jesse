# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# This file is used to define the routes to the strategies.
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

routes = [
    ('Binance Perpetual Futures', 'PAXG-USDT', '1m', 'Gold_Terminator'),
]

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# Extra candles are used to have more data for your strategies.
# For example, you might want to have more than one timeframe
# for one symbol, or you might want to have data for another
# symbol to use in your strategy's logic.
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
extra_candles = [
    # ('Binance Perpetual Futures', 'BTC-USDT', '1h'),
]
