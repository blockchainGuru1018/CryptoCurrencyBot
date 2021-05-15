import json
import requests as rq
import ccxt as ct


class CCXTApiHandler(object):
    """
    implementation of ccxt sdk
    for consuming data for the crypto bot
    """

    def __init__(self):
        self.supported_exchanges = {key: getattr(ct, key)
                                    for key in ct.exchanges}

    def load_exchange_manager(self, exchange, exchange_config={}):
        """
        loads the data_manager for
        the given exchange as long
        as it's supported by the app
        :param: str: exchange name
        :param exchange_config: dict: containing all needed
        configurations for the exchange to work.
        :return: object
        """
        assert exchange in self.supported_exchanges.keys(), \
            f"The exchange provided: {exchange} is not supported."
        return self.supported_exchanges[exchange](config=exchange_config)


    def get_exchange_fields(self, exchange_obj):
        """
        loads all of the usable fields for the given exchange
        and returns it in a json format
        :param exchange_obj: exchange object
        :return: JSON
        """
        fields = ["id","name","countries","urls","version","api","has","timeframes","timeout",
                  "rateLimit","userAgent","symbols","currencies","markets_by_id","apiKey","secret",
                  "password","uid"]
        return json.dumps({key: value for key,value in exchange_obj.__dict__() if key in fields})


    def list_markets(self, exchange_obj, params):
        """
        lists all of the markets available
        to the given exchange object
        :param exchange_obj:exchange object
        :param params: dict, params to get the market
        :return: list
        """
        return exchange_obj.fetch_markets(params=params)

    def get_market(self, exchange_obj, market_id, params):
        """
        gets an specific market from all supported
        markets in the exchange
        :param exchange_obj: exchange object
        :param market_id: str identifier of the market
        :param params: dict, params to get the market
        :return: dict
        """
        markets = self.list_markets(exchange_obj, params)
        for market in markets:
            if market['id'] == market_id:
                return market
        raise AttributeError(f"the specified market {market_id} doesn't exist"
                             ) from None

    def list_orders(self, exchange_obj):
        """
        provides a list of orders from
        the giben exhange object
        :param exchange_obj: exchange object
        :return: list
        """
        return exchange_obj.fetch_orders()

    def get_order(self, exchange_obj,order_id, params):
        """
        gets an specific oject on the orders book
        :param exchange_obj: exchange object
        :param order_id: str
        :param params: dict of parameters to pass to the object
        :return: dict
        """
        return exchange_obj.fetch_order(id=order_id, params=params)


    def list_currencies(self, exchange_obj):
        """
        provides a list of currencies available
        for the exchange given
        :param exchange_obj: exchange object
        :return: dict
        """
        return exchange_obj.fetch_currencies()


    def list_ohlcvs(self, exchange_obj, symbol, timeframe='1m',
                    since=None, limit=None, params={}):
        """
        gets all  ohlcv values for the
        given exchange with the given filters
        :param exchange_obj: exchange object
        :param symbol: identifier of the exhange or coin
        :param timeframe: time elapsed between entrance and value generated
        :param since: date to get from
        :param limit: date to get to
        :param params: dict, additional params for the fetching
        :return: dict
        """
        return exchange_obj.fetch_ohlcvc(symbol=symbol,
                                        timeframe=timeframe,
                                       since=since,
                                        limit=limit,
                                        params=params)

    def get_ohlcv(self,exchange_obj, symbol, timeframe='1m',
                    since=None, limit=None, params={}):
        """
        gets the ohlcv values for the
        given exchange
        :param exchange_obj: exchange object
        :param symbol: identifier of the exhange or coin
        :param timeframe: time elapsed between entrance and value generated
        :param since: date to get from
        :param limit: date to get to
        :param params: dict, additional params for the fetching
        :return: dict
        """
        return exchange_obj.fetch_ohlcv(symbol=symbol,
                                        timeframe=timeframe,
                                       since=since,
                                        limit=limit,
                                        params=params)


    def parse_ohlcv(self, exchange_obj, ohlcv):
        """
        parces the ohlcv values for the
         given exchange
        :param exchange_obj: exchange object
        :param ohlcv: ohlcv indication
        :return: dict
        """
        return exchange_obj.parse_ohlcv(ohlcv=ohlcv)

    def parse_ohlcvs(self, exchange_obj, ohlcvs, market=None, timeframe='1m',
                     since=None, limit=None):
        """
        parses all of the ohlcvs that matches the given filters
        based on the given exchange
        :param exchange_obj: exchange objects
        :param ohlcvs: list of ohlcvs
        :param market: marked selected
        :param timeframe: frequency of how hold it will get to load the intervals
        :param since: date to get from
        :param limit:date to get to
        :return: list
        """
        return exchange_obj.parse_ohlcvs(ohlcvs=ohlcvs, market=market, timeframe=timeframe,
                                         since=since, limit=limit)

