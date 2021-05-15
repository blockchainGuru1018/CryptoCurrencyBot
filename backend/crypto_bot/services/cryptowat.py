import json
import requests as req
import cryptowatch as cryp


class CryptoWatHandler(object):
    """
    This is a connector capable of consuming the SDK API
    provided by cryptowatch in order to manage your
    trading and crypto currency exchanges.
    more about the SDK here:
    https://github.com/cryptowatch/cw-sdk-python
    """
    def __init__(self, api_key, **kwargs):
        self.api_key = api_key
        self.kwargs = kwargs

    def authorize(self):
        """
        authorizes the app to access to the
        API resources.

        using the sdk, we you need to provide the api key
        in the .cw/credentials.yml file.

        after that only need to pass the data to the sdk
        :return: None
        """
        cryp.api_key = self.api_key


    def list_exchanges(self):
        """
        loads all of the exchanges of the client provided
        :return: List
        """
        return cryp.exchanges.list()

    def list_instruments(self):
        """
        loads all of the instruments of the client provided
        :return: List
        """
        return cryp.instruments.list()

    def list_markets(self):
        """
        loads all of the markets available of the client provided
        :return: List
        """
        return cryp.markets.list()


    def list_assets(self):
        """
        loads all of the assets of the client provided
        :return: List
        """
        return cryp.assets.list()

    def get_item(self, option, value):
        """
        gets a single value for the option given
        the options accepted are:
        -assets
        -instruments
        -exchanges
        :param option: str
        :param value: str : value to search from
        :return: http response object
        """
        options = {
            'assets': cryp.assets,
            'instruments':cryp.instruments,
            'exchanges':cryp.exchanges,
            'markets':cryp.markets
        }

        if option not in options.keys():
            raise AttributeError('The option provided is not recognized, the only options available are: {0}'.format([x for x in options.keys()]))
        return options[option].get(value)
