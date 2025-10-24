from typing import List
from ..repositories.exchange_repository import ExchangeRepository
from ..repositories.metrics_repository import MetricsRepository


class GetSymbolsUseCase:
    def __init__(self, exchange_repository: ExchangeRepository, metrics_repository: MetricsRepository):
        self.exchange_repository = exchange_repository
        self.metrics_repository = metrics_repository

    async def execute(self, exchange: str) -> dict:
        if not exchange:
            return {
                "status": 400,
                "msg": "Exchange não especificada."
            }

        if not isinstance(exchange, str) or exchange.strip() == "":
            return {
                "status": 400,
                "msg": "Exchange deve ser uma string válida."
            }

        available_exchanges = self.exchange_repository.get_available_exchanges()
        if exchange not in available_exchanges:
            return {
                "status": 404,
                "msg": "A exchange especificada não existe no momento na bridge."
            }

        try:
            symbols = await self.exchange_repository.get_symbols(exchange)
            await self.metrics_repository.record_exchange_access(exchange)

            return {
                "status": 200,
                "symbols": symbols
            }

        except Exception as e:
            print(f"Erro no getSymbols: {e}")
            return {
                "status": 500,
                "msg": "Erro interno do servidor ao buscar símbolos."
            }