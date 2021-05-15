import logging 

from bitcoin_arbitrage.monitor import settings
from bitcoin_arbitrage.monitor.exchange import Exchange
from bitcoin_arbitrage.monitor.log import setup_logger
from bitcoin_arbitrage.monitor.spread_detection import SpreadABC


logger = logging.getLogger(__name__)


class SpreadDifferentCurrenciesError(Exception):
    pass


class SpreadMissingPriceError(Exception):
    pass


class SpreadDetection(SpreadABC):

    def __init__(self, exchange_one: Exchange, exchange_two: Exchange):
        """
        To detect a spread it is necessary to have two exchanges or more.
        """
        if exchange_one.currency_pair != exchange_two.currency_pair:
            logger.debug('Spread between different currency pairs is not supported')
            raise SpreadDifferentCurrenciesError('Spread between different currency pairs is not supported')

        self.exchange_one = exchange_one
        self.exchange_two = exchange_two
        self.exchange_buy = None
        self.exchange_sell = None
        self.spread = self._calculate_spread()


    @property
    def summary(self):
        return f'{self.exchange_buy} [{self.exchange_buy.last_ask_price}] -> ' \
               f'{self.exchange_sell} [{self.exchange_sell.last_bid_price}] -> ' \
               f'Spread: {self.spread_with_currency}'


    @property
    def spread_with_currency(self):
        return f'{self.spread} {self.exchange_buy.currency_pair.fiat_symbol}'


    @property
    def spread_percentage(self):
        return self.spread / self.exchange_buy.last_bid_price


    def _calculate_spread(self):
        """
        The formula to calculate the spread is simple arithmetic.

        spread = (exchange one last bid price - exchange two last ask price)
                                    or
        spread = (exchange two last bid price - exchange one last ask price)

        Once that is calculated it is necessary to determine which one is greater than the other.
        to determine what action to take

        This determination is the return value of this method.
        """
        
        # if any of the necessary values is unavailale, a spread can not be calculated
        if None in [self.exchange_one.last_bid_price, self.exchange_one.last_ask_price,
                    self.exchange_two.last_bid_price, self.exchange_two.last_ask_price]:
            logger.warning('Cannot calculate this spread because one of the prices is missing.')
            raise SpreadMissingPriceError('Cannot calculate this spread because one of the prices is missing.')

        d1 = int(self.exchange_one.last_bid_price - self.exchange_two.last_ask_price)
        d2 = int(self.exchange_two.last_bid_price - self.exchange_one.last_ask_price)

        if d1 > d2:
            self.exchange_buy = self.exchange_two
            self.exchange_sell = self.exchange_one
            return d1
        else:
            self.exchange_buy = self.exchange_one
            self.exchange_sell = self.exchange_two
            return d2
