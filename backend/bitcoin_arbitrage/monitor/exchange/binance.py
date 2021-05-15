import logging 

from binance.client import Client

from bitcoin_arbitrage.monitor.api_keys import (
    BINANCE_API_KEY, 
    BINANCE_SECRET_KEY
)
from bitcoin_arbitrage.monitor.currency import CurrencyPair, FiatAmount
from bitcoin_arbitrage.monitor.exchange import Exchange, BTCAmount
from bitcoin_arbitrage.monitor.log import setup_logger
from bitcoin_arbitrage.monitor.order import Order, OrderState, OrderId


logger = logging.getLogger(__name__)


class Binance():

    def __init__(
        self, 
        api_key: str=BINANCE_API_KEY, 
        secret_key: str=BINANCE_SECRET_KEY
    ):
        self.client = Client(api_key, secret_key)


    def update_prices(self):
        try:
            self.tickers = self.client.get_orderbook_tickers()
        except Exception as error:
            logger.exception(str(error))
            return False
        return True

    def __str__(self):
        return f"{self.name}"


class BinanceAdapter(Exchange):

    currency_pair_api_representation = {
        CurrencyPair.BTC_USD: "BTCUSD",
        CurrencyPair.BTC_EUR: "BTCEUR",
        CurrencyPair.ETH_USD: "ETHUSD",
    }

    def __init__(self, currency_pair: CurrencyPair, binance: Binance):
        super().__init__(currency_pair)
        self.binance = binance
        self._depth = self.binance.client.get_order_book(symbol=currency_pair)        
        self.last_ask_price = float(self.depth['asks'][0][0])
        self.last_bid_price = float(self.depth['bids'][0][0])


    @property 
    def depth(self):
        return self._depth


    @depth.setter
    def depth(self, value):
        self._depth = value 


    @property
    def ticker_url(self):
        return f"{self.base_url}/pubticker/{self.currency_pair_api_representation[self.currency_pair]}"


    def limit_sell_order(self, amount: BTCAmount, limit: float):
        raise NotImplementedError


    def limit_buy_order(self, amount: BTCAmount, limit: float):
        raise NotImplementedError


    def get_order_state(self, order: Order):
        raise NotImplementedError
    

