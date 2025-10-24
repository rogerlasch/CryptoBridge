from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Optional


@dataclass
class ExchangeMetric:
    exchange_name: str
    request_count: int
    last_accessed: datetime
    created_at: Optional[datetime] = None

    def __post_init__(self):
        if self.created_at is None:
            self.created_at = datetime.now(timezone.utc)


@dataclass
class TickerMetric:
    exchange_name: str
    ticker_symbol: str
    request_count: int
    last_accessed: datetime
    created_at: Optional[datetime] = None

    def __post_init__(self):
        if self.created_at is None:
            self.created_at = datetime.now(timezone.utc)


@dataclass
class ApiMetric:
    endpoint: str
    method: str
    status_code: int
    response_time_ms: float
    timestamp: Optional[datetime] = None

    def __post_init__(self):
        if self.timestamp is None:
            self.timestamp = datetime.now(timezone.utc)