from abc import ABC, abstractmethod
from typing import List
from ..entities.metrics import ExchangeMetric, TickerMetric, ApiMetric


class MetricsRepository(ABC):

    @abstractmethod
    async def record_exchange_access(self, exchange_name: str) -> None:
        pass

    @abstractmethod
    async def record_ticker_access(self, exchange_name: str, ticker_symbol: str) -> None:
        pass

    @abstractmethod
    async def record_api_call(self, endpoint: str, method: str, status_code: int, response_time_ms: float) -> None:
        pass

    @abstractmethod
    async def get_top_exchanges(self, limit: int = 10) -> List[ExchangeMetric]:
        pass

    @abstractmethod
    async def get_top_tickers(self, limit: int = 10) -> List[TickerMetric]:
        pass

    @abstractmethod
    async def get_api_metrics_summary(self) -> dict:
        pass