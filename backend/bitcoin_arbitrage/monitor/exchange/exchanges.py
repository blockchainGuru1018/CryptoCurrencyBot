import ccxt

from bitcoin_arbitrage.monitor.currency import CurrencyPair
from bitcoin_arbitrage.monitor.exchange import Exchange, BTCAmount
from bitcoin_arbitrage.monitor.log import setup_logger
from bitcoin_arbitrage.monitor.order import Order, OrderState

logger = setup_logger('Binance')


class Hitbtc():

    def __init__(self):
        self.hitbtc = ccxt.hitbtc()


    @property
    def name(self):
        return str(self.__class__.__name__)


    def update_prices(self):
        try:
            self.tickers = self.hitbtc.fetch_ticers()
            return True
        except:
            return False

    def __str__(self):
        return f"{self.name}"


class HitbtcAdapter(Exchange):
    
    base_url = "test"
    currency_pair_api_representation = {
        CurrencyPair.BTC_USD: "BTCUSD",
        CurrencyPair.BTC_EUR: "BTCEUR",
        CurrencyPair.ETH_USD: "ETHUSD",
    }

    def __init__(self, currency_pair: CurrencyPair, hitbtc: Hitbtc):
        super().__init__(currency_pair)
        self.binance = binance
        depth = hitbtc.hitbtc.fetch_bids_asks(symbol=currency_pair)
        self.last_ask_price = 0
        self.last_bid_price = 0

    @property
    def ticker_url(self):
        return f"{self.base_url}/pubticker/{self.currency_pair_api_representation[self.currency_pair]}"


    def limit_sell_order(self, amount: BTCAmount, limit: float):
        raise NotImplementedError


    def limit_buy_order(self, amount: BTCAmount, limit: float):
        raise NotImplementedError


    def get_order_state(self, order: Order):
        raise NotImplementedError
