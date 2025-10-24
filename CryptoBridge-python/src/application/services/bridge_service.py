from typing import List
from ...domain.use_cases.get_exchanges import GetExchangesUseCase
from ...domain.use_cases.get_symbols import GetSymbolsUseCase
from ...domain.use_cases.get_tickers import GetTickersUseCase
from ...domain.repositories.exchange_repository import ExchangeRepository
from ...domain.repositories.metrics_repository import MetricsRepository


class BridgeService:
    def __init__(self, exchange_repository: ExchangeRepository, metrics_repository: MetricsRepository):
        self.get_exchanges_use_case = GetExchangesUseCase(exchange_repository)
        self.get_symbols_use_case = GetSymbolsUseCase(exchange_repository, metrics_repository)
        self.get_tickers_use_case = GetTickersUseCase(exchange_repository, metrics_repository)

    async def get_exchanges(self) -> dict:
        try:
            return await self.get_exchanges_use_case.execute()
        except Exception as e:
            print(f"Erro detalhado no BridgeService.get_exchanges: {str(e)}")
            return {
                "status": 500,
                "msg": "Erro interno do servidor."
            }

    async def get_symbols(self, exchange: str) -> dict:
        try:
            return await self.get_symbols_use_case.execute(exchange)
        except Exception as e:
            print(f"Erro detalhado no BridgeService.get_symbols: {str(e)}")
            return {
                "status": 500,
                "msg": "Erro interno do servidor."
            }

    async def get_tickers(self, exchange: str, tickers: List[str]) -> dict:
        try:
            return await self.get_tickers_use_case.execute(exchange, tickers)
        except Exception as e:
            print(f"Erro detalhado no BridgeService.get_tickers: {str(e)}")
            return {
                "status": 500,
                "msg": "Erro interno do servidor."
            }