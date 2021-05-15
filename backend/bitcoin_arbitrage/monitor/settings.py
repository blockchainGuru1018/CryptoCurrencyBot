import logging

LOG_LEVEL = logging.DEBUG


from bitcoin_arbitrage.monitor.currency import CurrencyPair

from bitcoin_arbitrage.monitor.exchange.bitfinex import Bitfinex
from bitcoin_arbitrage.monitor.exchange.bitstamp import Bitstamp
from bitcoin_arbitrage.monitor.exchange.gdax import Gdax
from bitcoin_arbitrage.monitor.exchange.binance import Binance

from bitcoin_arbitrage.monitor.update.db_commit import SpreadHistoryToDB
from bitcoin_arbitrage.monitor.update.csv_writer import AbstractSpreadToCSV


EXCHANGES = [
    Bitfinex(CurrencyPair.BTC_EUR),
    Bitstamp(CurrencyPair.BTC_EUR),
    Bitstamp(CurrencyPair.ETH_EUR),
    Gdax(CurrencyPair.BTC_EUR),
    Gdax(CurrencyPair.ETH_EUR),
]


BINANCE_API_KEY = "k2av5iKzXKDBbtD2TQ9c7jU6LoimCuyw6Hv5Eh51WwxQETqV9xthdeMV70nneJDX"
BINANCE_SECRET_KEY = "BVxDahg0GtqxrysiW3pTMT1zg0z9q9UtpXhk9sfzBnhRPsuiYCk7RhHOtuGrnBaD"

TRI_EXCHANGES = [
    {
        "name": "Binance",
        "exchange": Binance(),
        "currenciesList":[
            ['BNBBTC', 'ADABNB', 'ADABTC'],
            ['BNBBTC', 'ANTBNB', 'ANTBTC'],
            ['BNBBTC', 'ATOMBNB', 'ATOMBTC'],
            ['BNBBTC', 'AVABNB', 'AVABTC'],
            ['BNBBTC', 'AVAXBNB', 'AVAXBTC'],
        ],
    },
]


UPDATE_ACTIONS = [
    SpreadHistoryToDB(),
    AbstractSpreadToCSV('update_log.csv', True,),
]


UPDATE_INTERVAL = 5  # seconds

TIME_BETWEEN_NOTIFICATIONS = 5 * 60  # Only send a notification every 5 minutes

MINIMUM_SPREAD_TRADING = 200
TRADING_BTC_AMOUNT = 0.5
TRADING_LIMIT_PUFFER = 10  # Fiat Amount
TRADING_ORDER_STATE_UPDATE_INTERVAL = 1
TRADING_TIME_UNTIL_ORDER_CANCELLATION = 30

GDAX_KEY = "123123"
GDAX_SECRET = "123123"
GDAX_PASSPHRASE = "123123"
