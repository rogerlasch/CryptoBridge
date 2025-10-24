from datetime import datetime, timezone
from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, desc, update
from ...domain.repositories.metrics_repository import MetricsRepository
from ...domain.entities.metrics import ExchangeMetric, TickerMetric, ApiMetric
from ..database.models import ExchangeMetrics, TickerMetrics, ApiMetrics


class MetricsRepositoryImpl(MetricsRepository):
    def __init__(self, db_session: AsyncSession):
        self.db = db_session

    async def record_exchange_access(self, exchange_name: str) -> None:
        try:
            stmt = select(ExchangeMetrics).where(
                ExchangeMetrics.exchange_name == exchange_name
            )
            result = await self.db.execute(stmt)
            existing = result.scalar_one_or_none()

            if existing:
                stmt = update(ExchangeMetrics).where(
                    ExchangeMetrics.exchange_name == exchange_name
                ).values(
                    request_count=ExchangeMetrics.request_count + 1,
                    last_accessed=datetime.now(timezone.utc)
                )
                await self.db.execute(stmt)
            else:
                new_metric = ExchangeMetrics(
                    exchange_name=exchange_name,
                    request_count=1,
                    last_accessed=datetime.now(timezone.utc)
                )
                self.db.add(new_metric)

            await self.db.commit()
        except Exception as e:
            await self.db.rollback()
            print(f"Erro detalhado no MetricsRepositoryImpl.record_exchange_access para {exchange_name}: {str(e)}")
            raise

    async def record_ticker_access(self, exchange_name: str, ticker_symbol: str) -> None:
        try:
            stmt = select(TickerMetrics).where(
                TickerMetrics.exchange_name == exchange_name,
                TickerMetrics.ticker_symbol == ticker_symbol
            )
            result = await self.db.execute(stmt)
            existing = result.scalar_one_or_none()

            if existing:
                stmt = update(TickerMetrics).where(
                    TickerMetrics.exchange_name == exchange_name,
                    TickerMetrics.ticker_symbol == ticker_symbol
                ).values(
                    request_count=TickerMetrics.request_count + 1,
                    last_accessed=datetime.now(timezone.utc)
                )
                await self.db.execute(stmt)
            else:
                new_metric = TickerMetrics(
                    exchange_name=exchange_name,
                    ticker_symbol=ticker_symbol,
                    request_count=1,
                    last_accessed=datetime.now(timezone.utc)
                )
                self.db.add(new_metric)

            await self.db.commit()
        except Exception as e:
            await self.db.rollback()
            print(f"Erro detalhado no MetricsRepositoryImpl.record_ticker_access para {ticker_symbol} em {exchange_name}: {str(e)}")
            raise

    async def record_api_call(self, endpoint: str, method: str, status_code: int, response_time_ms: float) -> None:
        try:
            new_metric = ApiMetrics(
                endpoint=endpoint,
                method=method,
                status_code=status_code,
                response_time_ms=response_time_ms
            )
            self.db.add(new_metric)
            await self.db.commit()
        except Exception as e:
            await self.db.rollback()
            print(f"Erro detalhado no MetricsRepositoryImpl.record_api_call para {endpoint}: {str(e)}")
            raise

    async def get_top_exchanges(self, limit: int = 10) -> List[ExchangeMetric]:
        try:
            stmt = select(ExchangeMetrics).order_by(
                desc(ExchangeMetrics.request_count)
            ).limit(limit)

            result = await self.db.execute(stmt)
            metrics = result.scalars().all()

            return [
                ExchangeMetric(
                    exchange_name=m.exchange_name,
                    request_count=m.request_count,
                    last_accessed=m.last_accessed,
                    created_at=m.created_at
                )
                for m in metrics
            ]
        except Exception as e:
            print(f"Erro detalhado no MetricsRepositoryImpl.get_top_exchanges: {str(e)}")
            raise

    async def get_top_tickers(self, limit: int = 10) -> List[TickerMetric]:
        try:
            stmt = select(TickerMetrics).order_by(
                desc(TickerMetrics.request_count)
            ).limit(limit)

            result = await self.db.execute(stmt)
            metrics = result.scalars().all()

            return [
                TickerMetric(
                    exchange_name=m.exchange_name,
                    ticker_symbol=m.ticker_symbol,
                    request_count=m.request_count,
                    last_accessed=m.last_accessed,
                    created_at=m.created_at
                )
                for m in metrics
            ]
        except Exception as e:
            print(f"Erro detalhado no MetricsRepositoryImpl.get_top_tickers: {str(e)}")
            raise

    async def get_api_metrics_summary(self) -> dict:
        try:
            total_calls_stmt = select(func.count(ApiMetrics.id))
            avg_response_time_stmt = select(func.avg(ApiMetrics.response_time_ms))

            total_calls_result = await self.db.execute(total_calls_stmt)
            avg_response_time_result = await self.db.execute(avg_response_time_stmt)

            total_calls = total_calls_result.scalar()
            avg_response_time = avg_response_time_result.scalar()

            return {
                "total_api_calls": total_calls or 0,
                "average_response_time_ms": round(avg_response_time or 0, 2)
            }
        except Exception as e:
            print(f"Erro detalhado no MetricsRepositoryImpl.get_api_metrics_summary: {str(e)}")
            raise