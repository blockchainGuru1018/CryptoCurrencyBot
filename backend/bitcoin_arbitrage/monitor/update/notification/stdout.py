from typing import List

from bitcoin_arbitrage.monitor.exchange import Exchange
from bitcoin_arbitrage.monitor.log import setup_logger
from bitcoin_arbitrage.monitor.spread_detection.exchange import Spread_D
from bitcoin_arbitrage.monitor.spread_detection.triangular import Tri_Spread_D
from bitcoin_arbitrage.monitor.update.notification import NotificationService

logger = setup_logger('Stdout')


class StdoutNotification(NotificationService):
    def run(self, spreads: List[Spread_D], exchanges: List[Exchange], timestamp: float) -> None:
        if not self._should_notify(0):
            return
        spread = self._get_spread_for_notification(spreads)
        if spread is not None:
            print(f'Spread {spread.spread_with_currency} - {spread.summary}')
            
    '''Run triangular arbitrage.'''
    def run_tri(self, tri_spreads: List[Tri_Spread_D], exchanges: List[Exchange], timestamp: float) -> None:
        print('tri stdoutnotification running.')
        if not self._should_notify(0):
            return
        print('tri spread : ', tri_spreads)
        tri_spread = self._get_spread_for_notification(tri_spreads)
        if tri_spread is not None:
            print(f'Spread {tri_spread.spread_with_currency} - {tri_spread.summary}')
