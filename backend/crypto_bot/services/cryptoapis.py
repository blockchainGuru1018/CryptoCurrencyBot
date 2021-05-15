import requests as req
import json


class CryptoAPIsHandler(object):
    """
    This handler is about
     managing all apis coming from
     cryptoapis.io which are
     normally 3:
     Market data APIs
     Trading APIs
     Blockchain APIs

    """

    def __init__(self, api_key,option):
        self.api_key = api_key
        self.option = option
        self.endpoints = {
            'root': 'https://api.cryptoapis.io'
        }


