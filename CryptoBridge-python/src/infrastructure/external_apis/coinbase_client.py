import asyncio
from typing import List, Optional, Dict, Any
import httpx
from ...domain.entities.ticker import Ticker


class CoinbaseClient:
    BaseUrl = "https://api.exchange.coinbase.com/products"

    def __init__(self):
        self.timeout = httpx.Timeout(10.0, connect=5.0)

    async def getSymbols(self) -> List[str]:
        try:
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                response = await client.get(self.BaseUrl)

                if response.status_code != 200:
                    return []

                data = response.json()
                return [product["id"] for product in data]

        except Exception as e:
            print(f"Erro ao buscar símbolos no Coinbase: {e}")
            return []

    async def getTicker(self, symbol: str) -> Optional[Ticker]:
        try:
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                stats_task = client.get(f"{self.BaseUrl}/{symbol}/stats")
                ticker_task = client.get(f"{self.BaseUrl}/{symbol}/ticker")

                stats_response, ticker_response = await asyncio.gather(
                    stats_task, ticker_task, return_exceptions=True
                )

                if (isinstance(stats_response, Exception) or
                    isinstance(ticker_response, Exception) or
                    stats_response.status_code != 200 or
                    ticker_response.status_code != 200):
                    return None

                stats_data = stats_response.json()
                ticker_data = ticker_response.json()

                return Ticker(
                    symbol=symbol,
                    buy=float(ticker_data.get("bid", 0)),
                    sell=float(ticker_data.get("ask", 0)),
                    vol=float(stats_data.get("volume", 0)),
                    low=float(stats_data.get("low", 0)),
                    high=float(stats_data.get("high", 0)),
                    last=float(ticker_data.get("price", 0))
                )

        except Exception as e:
            print(f"Erro ao buscar ticker {symbol} no Coinbase: {e}")
            return None