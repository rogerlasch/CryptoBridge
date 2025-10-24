import asyncio
import time
from typing import Optional, Any, Dict, Tuple


class MemoryCache:
    def __init__(self, ttl_seconds: int = 60):
        self._cache: Dict[str, Tuple[Any, float]] = {}
        self._ttl = ttl_seconds
        self._lock = asyncio.Lock()
        print(f"Iniciando sistema de cache com TTL={ttl_seconds} segundos")

    async def get(self, key: str) -> Optional[Any]:
        async with self._lock:
            if key in self._cache:
                value, timestamp = self._cache[key]
                if time.time() - timestamp < self._ttl:
                    return value
                del self._cache[key]
            return None

    async def set(self, key: str, value: Any) -> None:
        async with self._lock:
            self._cache[key] = (value, time.time())

    async def delete(self, key: str) -> None:
        async with self._lock:
            if key in self._cache:
                del self._cache[key]

    async def clear(self) -> None:
        async with self._lock:
            self._cache.clear()

    async def size(self) -> int:
        async with self._lock:
            return len(self._cache)