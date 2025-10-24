import pytest
import asyncio
import sys
import os
from httpx import AsyncClient

# Add the parent directory to Python path to import main
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from main import app
from src.infrastructure.database.connection import engine, Base
from src.infrastructure.database import models  # Import models to register them


@pytest.fixture(scope="session")
def event_loop():
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="session")
async def setup_database():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest.fixture
async def client(setup_database):
    async with AsyncClient(app=app, base_url="http://test") as ac:
        yield ac