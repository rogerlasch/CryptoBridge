from typing import List
from ...domain.repositories.metrics_repository import MetricsRepository
from ...domain.entities.metrics import ExchangeMetric, TickerMetric


class MetricsService:
    def __init__(self, metrics_repository: MetricsRepository):
        self.metrics_repository = metrics_repository

    async def record_api_call(self, endpoint: str, method: str, status_code: int, response_time_ms: float) -> None:
        try:
            await self.metrics_repository.record_api_call(endpoint, method, status_code, response_time_ms)
        except Exception as e:
            print(f"Erro detalhado no MetricsService.record_api_call: {str(e)}")

    async def get_top_exchanges(self, limit: int = 10) -> dict:
        try:
            exchanges = await self.metrics_repository.get_top_exchanges(limit)
            return {
                "status": 200,
                "top_exchanges": [
                    {
                        "exchange_name": e.exchange_name,
                        "request_count": e.request_count,
                        "last_accessed": e.last_accessed.isoformat(),
                        "created_at": e.created_at.isoformat()
                    }
                    for e in exchanges
                ]
            }
        except Exception as e:
            print(f"Erro detalhado no MetricsService.get_top_exchanges: {str(e)}")
            return {
                "status": 500,
                "msg": "Erro interno do servidor."
            }

    async def get_top_tickers(self, limit: int = 10) -> dict:
        try:
            tickers = await self.metrics_repository.get_top_tickers(limit)
            return {
                "status": 200,
                "top_tickers": [
                    {
                        "exchange_name": t.exchange_name,
                        "ticker_symbol": t.ticker_symbol,
                        "request_count": t.request_count,
                        "last_accessed": t.last_accessed.isoformat(),
                        "created_at": t.created_at.isoformat()
                    }
                    for t in tickers
                ]
            }
        except Exception as e:
            print(f"Erro detalhado no MetricsService.get_top_tickers: {str(e)}")
            return {
                "status": 500,
                "msg": "Erro interno do servidor."
            }

    async def get_performance_metrics(self) -> dict:
        try:
            summary = await self.metrics_repository.get_api_metrics_summary()
            return {
                "status": 200,
                "performance": summary
            }
        except Exception as e:
            print(f"Erro detalhado no MetricsService.get_performance_metrics: {str(e)}")
            return {
                "status": 500,
                "msg": "Erro interno do servidor."
            }

    async def get_summary(self) -> dict:
        try:
            top_exchanges = await self.metrics_repository.get_top_exchanges(5)
            top_tickers = await self.metrics_repository.get_top_tickers(5)
            performance = await self.metrics_repository.get_api_metrics_summary()

            return {
                "status": 200,
                "summary": {
                    "top_5_exchanges": [
                        {
                            "exchange_name": e.exchange_name,
                            "request_count": e.request_count
                        }
                        for e in top_exchanges
                    ],
                    "top_5_tickers": [
                        {
                            "exchange_name": t.exchange_name,
                            "ticker_symbol": t.ticker_symbol,
                            "request_count": t.request_count
                        }
                        for t in top_tickers
                    ],
                    "performance": performance
                }
            }
        except Exception as e:
            print(f"Erro detalhado no MetricsService.get_summary: {str(e)}")
            return {
                "status": 500,
                "msg": "Erro interno do servidor."
            }