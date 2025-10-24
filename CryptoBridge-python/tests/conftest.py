import pytest
import asyncio
import os
from httpx import AsyncClient


class TestConfig:
    SERVER_URL = os.getenv("TEST_SERVER_URL", "http://localhost:3000")
    TIMEOUT = 30.0


@pytest.fixture(scope="session")
def event_loop():
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture
async def client():
    async with AsyncClient(base_url=TestConfig.SERVER_URL, timeout=TestConfig.TIMEOUT) as ac:
        yield ac


@pytest.fixture
async def server_health_check():
    async with AsyncClient(base_url=TestConfig.SERVER_URL, timeout=5.0) as client:
        try:
            response = await client.get("/")
            assert response.status_code == 200
        except Exception as e:
            pytest.fail(f"Server not running at {TestConfig.SERVER_URL}: {e}")