import asyncio
from typing import List, Optional, Dict, Any
import httpx
from ...domain.entities.ticker import Ticker


class MercadoBitcoinClient:
    BaseUrl = "https://api.mercadobitcoin.net/api/v4"

    def __init__(self):
        self.timeout = httpx.Timeout(10.0, connect=5.0)

    async def getSymbols(self) -> List[str]:
        try:
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                response = await client.get(f"{self.BaseUrl}/symbols")

                if response.status_code != 200:
                    return []

                data = response.json()
                return data.get("symbol", [])

        except Exception as e:
            print(f"Erro ao buscar símbolos no Mercado Bitcoin: {e}")
            return []

    async def getTicker(self, symbol: str) -> Optional[Ticker]:
        try:
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                response = await client.get(f"{self.BaseUrl}/tickers?symbols={symbol}")

                if response.status_code != 200:
                    return None

                data = response.json()

                if not data or len(data) == 0:
                    return None

                ticker_data = data[0]

                return Ticker(
                    symbol=symbol,
                    buy=float(ticker_data.get("buy", 0)),
                    sell=float(ticker_data.get("sell", 0)),
                    vol=float(ticker_data.get("vol", 0)),
                    low=float(ticker_data.get("low", 0)),
                    high=float(ticker_data.get("high", 0)),
                    last=float(ticker_data.get("last", 0))
                )

        except Exception as e:
            print(f"Erro ao buscar ticker {symbol} no Mercado Bitcoin: {e}")
            return None