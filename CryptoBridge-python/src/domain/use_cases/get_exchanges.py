from typing import List
from ..repositories.exchange_repository import ExchangeRepository


class GetExchangesUseCase:
    def __init__(self, exchange_repository: ExchangeRepository):
        self.exchange_repository = exchange_repository

    async def execute(self) -> dict:
        try:
            exchanges = self.exchange_repository.get_available_exchanges()
            return {
                "status": 200,
                "exchanges": exchanges
            }
        except Exception as e:
            print(f"Erro detalhado no GetExchangesUseCase: {str(e)}")
            return {
                "status": 500,
                "msg": "Erro interno do servidor."
            }