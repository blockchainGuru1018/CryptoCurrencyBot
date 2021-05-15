from bitcoin_arbitrage.monitor import settings
from bitcoin_arbitrage.monitor.exchange import Exchange
from bitcoin_arbitrage.monitor.log import setup_logger
from bitcoin_arbitrage.monitor.spread_detection import SpreadABC


logger = setup_logger('tri_spread_d')


class TriSpreadDifferentCurrenciesError(Exception):
    pass


class TriSpreadMissingPriceError(Exception):
    pass


class TriSpreadDetector(SpreadABC):


    def __init__(self, exchange: Exchange, currenciesList: list):
        self.exchange = exchange
        self.currenciesList = currenciesList
        self.spread = self._calculate_spread()


    @property
    def summary(self):
        return f'Tri_Spread: {self.spread_with_currency}'


    @property
    def spread_with_currency(self):
        return f'{self.spread}'


    @property
    def spread_percentage(self):
        return self.spread


    def _calculate_spread(self):
        exch_rate_list = []
        client = self.exchange.client
        sym = self.currenciesList[0]
        depth = client.get_order_book(symbol=sym)
        price1 = float(depth['bids'][0][0])
        exch_rate_list.append(price1)

        sym = self.currenciesList[1]
        currency_pair = "Currency Pair: "+str(sym)+" "
        try:
            depth = client.get_order_book(symbol=sym)
            price2 = float(depth['asks'][0][0])
            price2 = 1/price2
            exch_rate_list.append(price2)
        except Exception as error:
            logger.exception(str(error))
            price2 = 0.000000001
            exch_rate_list.append(price2)  

        sym = self.currenciesList[2]
        currency_pair = "Currency Pair: "+str(sym)+" "
        depth = client.get_order_book(symbol=sym)
        price3 = float(depth['bids'][0][0])
        exch_rate_list.append(price3)

        rate1 = exch_rate_list[0]
        buy_price = "Buy: {}".format(rate1)
        rate2 = price3 * price2
        sell_price = "Sell: {}".format(rate2)
        if float(rate1) < float(rate2):
            print('Detecting the opportunities for triangular arbitrage trading.', self.currenciesList)
        else:
            print("No Arbitrage Possibility")

        return float(rate2) - float(rate1)
