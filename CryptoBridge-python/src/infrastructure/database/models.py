from datetime import datetime
from sqlalchemy import Column, Integer, String, Float, DateTime
from .connection import Base


class ExchangeMetrics(Base):
    __tablename__ = "exchange_metrics"

    id = Column(Integer, primary_key=True, index=True)
    exchange_name = Column(String(50), nullable=False, index=True)
    request_count = Column(Integer, default=0, nullable=False)
    last_accessed = Column(DateTime, default=datetime.utcnow, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)


class TickerMetrics(Base):
    __tablename__ = "ticker_metrics"

    id = Column(Integer, primary_key=True, index=True)
    exchange_name = Column(String(50), nullable=False, index=True)
    ticker_symbol = Column(String(20), nullable=False, index=True)
    request_count = Column(Integer, default=0, nullable=False)
    last_accessed = Column(DateTime, default=datetime.utcnow, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)


class ApiMetrics(Base):
    __tablename__ = "api_metrics"

    id = Column(Integer, primary_key=True, index=True)
    endpoint = Column(String(100), nullable=False, index=True)
    method = Column(String(10), nullable=False)
    status_code = Column(Integer, nullable=False)
    response_time_ms = Column(Float, nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow, nullable=False)