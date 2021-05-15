import request as req
import json
from binance.client import Client



class BinaceAPIHandler(object):
    """
    Binace web service consumption
    for the application.
    """
    def __init__(self, api_key, secret):
        self.api_key = api_key
        self.secret = secret
        self.endpoints = {
            'root': "https://api.binance.com"
        }
        self.handler = self.load_handler()

    def load_handler(self):
        """
        loads the handler for the consumption to
        use for the api itself.
        :return: binace client object
        """
        return Client(api_key=self.api_key, api_secret=self.secret)


    def get_wallet_coins(self):
        """
        gets all of the available coins
        details
        :return:list
        """
