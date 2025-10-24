from typing import List
from ..repositories.exchange_repository import ExchangeRepository
from ..repositories.metrics_repository import MetricsRepository


class GetTickersUseCase:
    def __init__(self, exchange_repository: ExchangeRepository, metrics_repository: MetricsRepository):
        self.exchange_repository = exchange_repository
        self.metrics_repository = metrics_repository

    async def execute(self, exchange: str, tickers: List[str]) -> dict:
        if not exchange or not tickers:
            return {
                "status": 400,
                "msg": "O parâmetro exchange ou tickers não foi especificado corretamente."
            }

        if not isinstance(tickers, list):
            return {
                "status": 400,
                "msg": "O parâmetro tickers não é um array válido."
            }

        if len(tickers) == 0:
            return {
                "status": 400,
                "msg": "O array de tickers não pode estar vazio."
            }

        for ticker in tickers:
            if not isinstance(ticker, str) or ticker.strip() == "":
                return {
                    "status": 400,
                    "msg": "Todos os tickers devem ser strings válidas."
                }

        available_exchanges = self.exchange_repository.get_available_exchanges()
        if exchange not in available_exchanges:
            return {
                "status": 404,
                "msg": "A exchange especificada ainda não está disponível na bridge."
            }

        try:
            result = []
            await self.metrics_repository.record_exchange_access(exchange)

            for ticker in tickers:
                ticker_data = await self.exchange_repository.get_ticker(exchange, ticker)

                if ticker_data:
                    await self.metrics_repository.record_ticker_access(exchange, ticker)
                    result.append({
                        "symbol": ticker_data.symbol,
                        "buy": ticker_data.buy,
                        "sell": ticker_data.sell,
                        "vol": ticker_data.vol,
                        "low": ticker_data.low,
                        "high": ticker_data.high,
                        "last": ticker_data.last
                    })

            return {
                "status": 200,
                "tickers": result
            }

        except Exception as e:
            print(f"Erro no getTickers: {e}")
            return {
                "status": 500,
                "msg": "Erro interno do servidor ao buscar tickers."
            }