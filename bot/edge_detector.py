"""Keeps best bid/ask for each exchange+symbol and fires callback when arbitrage edge appears."""
from collections import defaultdict
from typing import Callable
from .config import settings

class EdgeDetector:
    def __init__(self, on_edge: Callable):
        self.best_bid = defaultdict(lambda: defaultdict(lambda: None))  # exch->sym->price
        self.best_ask = defaultdict(lambda: defaultdict(lambda: None))
        self.on_edge  = on_edge

    def update(self, exchange: str, symbol: str, bid: float, ask: float):
        self.best_bid[exchange][symbol] = bid
        self.best_ask[exchange][symbol] = ask
        self._check_edges(symbol)

    def _check_edges(self, symbol: str):
        # iterate over all pairs of exchanges
        for src in settings.EXCHANGES:
            for dst in settings.EXCHANGES:
                if src == dst:
                    continue
                bid = self.best_bid[dst].get(symbol)
                ask = self.best_ask[src].get(symbol)
                if bid and ask:
                    edge = (bid - ask) / ask
                    if edge > settings.EDGE_THRESH:
                        self.on_edge(symbol, src, dst, ask, bid, edge)
