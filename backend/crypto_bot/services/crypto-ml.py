import requests as req
import json

class CryptoMLHandler:
    def __init__(self, api_key, secret):
        """
        implementation of cryptoML wrapper
        :param api_key: str
        :param secret: str
        """
        self.api_key = api_key
        self.secret = secret
        self.access_token = None
        self.endpoints = {
            'root':'',
            'auth':'',
        }