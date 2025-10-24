from dataclasses import dataclass
from typing import Optional


@dataclass
class Ticker:
    symbol: str
    buy: float
    sell: float
    vol: float
    low: float
    high: float
    last: float

    def __post_init__(self):
        if not self.symbol or not isinstance(self.symbol, str):
            raise ValueError("Symbol must be a non-empty string")

        for field in ['buy', 'sell', 'vol', 'low', 'high', 'last']:
            value = getattr(self, field)
            if not isinstance(value, (int, float)) or value < 0:
                setattr(self, field, 0.0)