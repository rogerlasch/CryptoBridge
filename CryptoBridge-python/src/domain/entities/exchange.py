from dataclasses import dataclass
from typing import List


@dataclass
class Exchange:
    name: str
    symbols: List[str]

    def __post_init__(self):
        if not self.name or not isinstance(self.name, str):
            raise ValueError("Exchange name must be a non-empty string")

        if not isinstance(self.symbols, list):
            self.symbols = []

    def has_symbol(self, symbol: str) -> bool:
        return symbol in self.symbols