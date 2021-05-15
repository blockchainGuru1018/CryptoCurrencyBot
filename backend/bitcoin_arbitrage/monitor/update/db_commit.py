import logging
import pdb

from typing import List

from bitcoin_arbitrage.models import Spread, Exchange, Tri_Spread
from bitcoin_arbitrage.monitor.update import UpdateAction
from bitcoin_arbitrage.monitor.spread_detection.exchange import SpreadDetection
from bitcoin_arbitrage.monitor.spread_detection.triangular import TriSpreadDetector
from bitcoin_arbitrage.monitor.exchange.binance import BinanceAdapter


logger = logging.getLogger(__name__)


class SpreadHistoryToDB(UpdateAction):

    def run_spread(
        self, 
        spreads: List[SpreadDetection], 
        exchanges: List[Exchange], 
        timestamp: float
    ):
        for spread in spreads:
            try:
                Exchange.objects.create(
                    name=spread.exchange_buy.name,
                    currency_pair=spread.exchange_buy.currency_pair,
                    last_ask_price=spread.exchange_buy.last_ask_price,
                    last_bid_price=spread.exchange_buy.last_bid_price
                )
                Exchange.objects.create(
                    name=spread.exchange_sell.name,
                    currency_pair=spread.exchange_sell.currency_pair,
                    last_ask_price=spread.exchange_sell.last_ask_price,
                    last_bid_price=spread.exchange_sell.last_bid_price
                )
                Spread.objects.create(
                    spread=spread.spread,
                    xchange_buy=exchange_buy,
                    xchange_sell=exchange_sell
                )
            except Exception as error:
                logger.exception(str(error))
                continue 

   
    def run_tri(self, tri_spreads: List[TriSpreadDetector], tri_exchanges: List[Exchange], timestamp: float):
        for spread in tri_spreads:
            try:
                binance_buy1 = BinanceAdapter(
                    spread.currenciesList[0], 
                    spread.exchange
                )
                tri_exchange_buy1 = Exchange.objects.create(
                    name=binance_buy1.name,
                    currency_pair=binance_buy1.currency_pair,
                    last_ask_price=binance_buy1.last_ask_price,
                    last_bid_price=binance_buy1.last_bid_price
                )
                binance_sell = BinanceAdapter(
                    spread.currenciesList[1], 
                    spread.exchange
                )
                tri_exchange_sell = Exchange.objects.create(
                    name=binance_sell.name,
                    currency_pair=binance_sell.currency_pair,
                    last_ask_price=binance_sell.last_ask_price,
                    last_bid_price=binance_sell.last_bid_price
                )
                binance_buy2 = BinanceAdapter(
                    spread.currenciesList[2], 
                    spread.exchange
                )
                tri_exchange_buy2 = Exchange.objects.create(
                    name=binance_buy2.name,
                    currency_pair=binance_buy2.currency_pair,
                    last_ask_price=binance_buy2.last_ask_price,
                    last_bid_price=binance_buy2.last_bid_price
                )
                tri_spread = Tri_Spread.objects.create(
                    tri_spread=spread.spread,
                    tri_xchange_buy1=tri_exchange_buy1,
                    tri_xchange_buy2=tri_exchange_buy2,
                    tri_xchange_sell=tri_exchange_sell
                )
            except Exception as error:
                logger.exception(str(error))
                continue     

    def save_inter(self, inter_spreads, inter_exchanges):
        pass 
