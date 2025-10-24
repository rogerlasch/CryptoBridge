from typing import List
from pydantic import BaseModel, Field


class TickerRequest(BaseModel):
    exchange: str = Field(..., min_length=1, description="Nome da exchange")
    tickers: List[str] = Field(..., min_length=1, description="Lista de símbolos de tickers")


class SymbolRequest(BaseModel):
    exchange: str = Field(..., min_length=1, description="Nome da exchange")


class TickerResponse(BaseModel):
    symbol: str
    buy: float
    sell: float
    vol: float
    low: float
    high: float
    last: float


class TickersResponse(BaseModel):
    status: int
    tickers: List[TickerResponse]


class SymbolsResponse(BaseModel):
    status: int
    symbols: List[str]


class ExchangesResponse(BaseModel):
    status: int
    exchanges: List[str]


class ErrorResponse(BaseModel):
    status: int
    msg: str