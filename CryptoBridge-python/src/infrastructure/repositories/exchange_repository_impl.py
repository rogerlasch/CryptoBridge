from typing import List, Optional
from ...domain.repositories.exchange_repository import ExchangeRepository
from ...domain.entities.ticker import Ticker
from ..external_apis.mercado_bitcoin_client import MercadoBitcoinClient
from ..external_apis.coinbase_client import CoinbaseClient
from ..cache.memory_cache import MemoryCache


class ExchangeRepositoryImpl(ExchangeRepository):
    def __init__(self):
        self.clients = {
            "mercadobitcoin": MercadoBitcoinClient(),
            "coinbase": CoinbaseClient()
        }
        self.cache = MemoryCache(ttl_seconds=60)

    def get_available_exchanges(self) -> List[str]:
        return list(self.clients.keys())

    async def get_symbols(self, exchange: str) -> List[str]:
        try:
            if exchange not in self.clients:
                return []

            cache_key = f"symbols-{exchange}"
            cached_symbols = await self.cache.get(cache_key)

            if cached_symbols:
                return cached_symbols

            client = self.clients[exchange]
            symbols = await client.getSymbols()

            if symbols:
                await self.cache.set(cache_key, symbols)

            return symbols
        except Exception as e:
            print(f"Erro detalhado no ExchangeRepositoryImpl.get_symbols para {exchange}: {str(e)}")
            return []

    async def get_ticker(self, exchange: str, symbol: str) -> Optional[Ticker]:
        try:
            if exchange not in self.clients:
                return None

            cache_key = f"ticker-{exchange}-{symbol}"
            cached_ticker = await self.cache.get(cache_key)

            if cached_ticker:
                return cached_ticker

            client = self.clients[exchange]
            ticker = await client.getTicker(symbol)

            if ticker:
                await self.cache.set(cache_key, ticker)

            return ticker
        except Exception as e:
            print(f"Erro detalhado no ExchangeRepositoryImpl.get_ticker para {symbol} em {exchange}: {str(e)}")
            return None