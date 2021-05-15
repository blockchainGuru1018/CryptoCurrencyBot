from abc import ABC, abstractmethod
from typing import List, Optional

from bitcoin_arbitrage.monitor.exchange import Exchange
from bitcoin_arbitrage.monitor.spread_detection.exchange import SpreadDetection

from bitcoin_arbitrage.monitor.spread_detection.triangular import TriSpreadDetector


class UpdateAction(ABC):
    def __init__(self, spread_threshold: Optional[int]=None):
        self.threshold = spread_threshold or 0

    def run_inter(self, spreads: List[SpreadDetection], exchanges: List[Exchange], timestamp: float):
        raise NotImplementedError

    def run_tri(self, spreads: List[TriSpreadDetector], exchanges: List[Exchange], timestamp: float):
        raise NotImplementedError
