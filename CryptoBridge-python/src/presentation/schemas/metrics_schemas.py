from typing import List, Dict, Any
from pydantic import BaseModel
from datetime import datetime


class ExchangeMetricResponse(BaseModel):
    exchange_name: str
    request_count: int
    last_accessed: str
    created_at: str


class TickerMetricResponse(BaseModel):
    exchange_name: str
    ticker_symbol: str
    request_count: int
    last_accessed: str
    created_at: str


class TopExchangesResponse(BaseModel):
    status: int
    top_exchanges: List[ExchangeMetricResponse]


class TopTickersResponse(BaseModel):
    status: int
    top_tickers: List[TickerMetricResponse]


class PerformanceResponse(BaseModel):
    status: int
    performance: Dict[str, Any]


class SummaryResponse(BaseModel):
    status: int
    summary: Dict[str, Any]