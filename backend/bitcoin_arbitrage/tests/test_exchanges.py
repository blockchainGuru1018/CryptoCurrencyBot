from django.test import TestCase

from bitcoin_arbitrage.monitor.exchange.binance import BinanceAdapter
from bitcoin_arbitrage.monitor.exchange.bitfinex import Bitfinex
from bitcoin_arbitrage.monitor.exchange.bitstamp import Bitstamp
from bitcoin_arbitrage.monitor.exchange.gdax import Gdax


logger = logging.getLogger(__name__)



class TestBinanceExchange(TestCase):
    def setUp(self):
        pass 


class TestBitFinexExchange(TestCase):
    def setUp(self):
        pass 
 

class TestBitStampExchange(TestCase):
    def setUp(self):
        pass 


class TestGdaxExchange(TestCase):
    def setUp(self):
        pass 