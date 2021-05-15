import json
import logging
import sys

from abc import ABC, abstractmethod
from typing import Optional

import requests

from bitcoin_arbitrage.monitor.currency import CurrencyPair, BTCAmount
from bitcoin_arbitrage.monitor.order import Order, OrderState


logger = logging.getLogger(__name__)


class Exchange(ABC):
    def __init__(self, currency_pair: CurrencyPair):
        self.currency_pair = currency_pair
        self.last_ask_price: Optional[float] = None
        self.last_bid_price: Optional[float] = None

    
    @property
    def name(self):
        class_name = str(self.__class__.__name__)
        if "adapter" in class_name.lower():
            class_name = class_name.replace("Adapter", "")
        return class_name


    @property
    def summary(self):
        return self.__str__() + f"\n - Ask: {self.last_ask_price}" \
                                f"\n - Bid: {self.last_bid_price}"
    
    @property
    def currency_pair_api_representation(self):
        raise NotImplementedError


    @property
    def ticker_url(self):
        raise NotImplementedError

    
    @property
    def base_url(self):
        raise NotImplementedError


    def limit_buy_order(self, amount: BTCAmount, limit: float):
        raise NotImplementedError


    def limit_sell_order(self, amount: BTCAmount, limit: float):
        raise NotImplementedError

    
    def get_order_state(self, order: Order):
        raise NotImplementedError


    def cancel_order(self, order: Order):
        raise NotImplementedError


    def update_prices(self):
        print('Geting url : ', self.ticker_url)
        response = requests.get(self.ticker_url)
        if response.status_code != 200:
            logger.warning('Could not update prices. API returned status != 200.')
            return
        try:
            json_response = response.json()
            self.last_ask_price = float(json_response.get('ask'))
            self.last_bid_price = float(json_response.get('bid'))
        except json.decoder.JSONDecodeError or TypeError:
            logger.error('Could not update prices. Error on json processing:')
            logger.error(sys.exc_info())


    def __str__(self):
        return f"{self.name} ({self.currency_pair.value})"
