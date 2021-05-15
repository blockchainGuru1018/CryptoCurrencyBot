import itertools
import logging

from datetime import datetime
from time import sleep 
from typing import List

from bitcoin_arbitrage.models import Spread
from bitcoin_arbitrage.monitor import settings
from bitcoin_arbitrage.monitor.exchange import Exchange
from bitcoin_arbitrage.monitor.log import setup_logger
from bitcoin_arbitrage.monitor.spread_detection.exchange import (
    SpreadDetection, 
    SpreadMissingPriceError, 
    SpreadDifferentCurrenciesError
)
from bitcoin_arbitrage.monitor.spread_detection.triangular import (
    TriSpreadDetector, 
    TriSpreadMissingPriceError
)



logger = logging.getLogger(__name__)


class Monitor:

    def __init__(self):
        self._last_spreads: List[Spread] = []


    def update_tri(self):
        while True:
            try:
                # update prices of exchanges 
                for tri_exchange in settings.TRI_EXCHANGES:
                    tri_exchange['exchange'].update_prices()

                # calculation tri_spreads using triangular arbitrage.
                tri_spreads = self._calculate_tri_spreads()

                # Action on triangular arbitrage
                timestamp = datetime.now().timestamp()
                for action in settings.UPDATE_ACTIONS:
                    action.run_tri(tri_spreads, settings.TRI_EXCHANGES, timestamp)

                sleep(settings.UPDATE_INTERVAL)
            except Exception as error:
                # Log the exception to be able to identify unknown exceptions in
                # order to handle them according to their type.
                logger.exception(str(error))
                continue 


    def update_inter(self):
        while True:
            try:
                # Update prices of exchanges            
                for exchange in settings.EXCHANGES:
                    exchange.update_prices()
                # Calculation spreads using exchange arbitrage.
                spreads = self._calculate_spreads()
            
                # Action on exchange arbitrage
                timestamp = datetime.now().timestamp()
            
                # Saves interexchange to database and csv
                for action in settings.UPDATE_ACTIONS:
                    action.run_inter(spreads, settings.EXCHANGES, timestamp)       
            
                sleep(settings.UPDATE_INTERVAL)
            except Exception as update_error:
                logger.exception(str(update_error))
                continue


    def _calculate_spreads(self):
        combinations: List[(Exchange, Exchange)] = itertools.combinations(settings.EXCHANGES, 2)
        spreads = []
        for pair in combinations:
            try:
                spread = SpreadDetection(exchange_one=pair[0], exchange_two=pair[1])
                spreads.append(spread)
            except (SpreadMissingPriceError, SpreadDifferentCurrenciesError) as error:
                # Set exception handlers here for Missing Prices and Differenct
                # Currencies Errors, we still do not have these.
                logger.exception(str(error))
            except Exception as error:
                # General exception handling, we can get a better idea of what
                # exceptions can occurr.
                logger.exception(str(error))
        return spreads

    
    def _calculate_tri_spreads(self):
        tri_spreads: List[TriSpreadDetector] = []
        for tri_exchange in settings.TRI_EXCHANGES:
            try:
                for currenciesList in tri_exchange['currenciesList']:
                    try:
                        tri_spread = TriSpreadDetector(
                            exchange=tri_exchange['exchange'], 
                            currenciesList=currenciesList
                        )
                        tri_spreads.append(tri_spread)
                    except (TriSpreadMissingPriceError) as missing_price_error:
                        # Add a strategy for this exception.
                        logger.exception(str(missing_price_error))
                        continue 
                    except Exception as error:
                        # Log general exceptions to see what type of exception is and
                        # handle it according to a strategy.
                        logger.exception(str(error))
                        continue
            except Exception as tri_exchange_error:
                logger.exception(str(tri_exchange_error))
                
        return tri_spreads
