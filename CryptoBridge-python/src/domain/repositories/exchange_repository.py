from abc import ABC, abstractmethod
from typing import List, Optional
from ..entities.ticker import Ticker


class ExchangeRepository(ABC):

    @abstractmethod
    async def get_symbols(self, exchange: str) -> List[str]:
        pass

    @abstractmethod
    async def get_ticker(self, exchange: str, symbol: str) -> Optional[Ticker]:
        pass

    @abstractmethod
    def get_available_exchanges(self) -> List[str]:
        pass