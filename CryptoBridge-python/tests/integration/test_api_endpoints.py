import pytest
from httpx import AsyncClient


class TestExchangeEndpoints:
    @pytest.mark.asyncio
    async def test_get_exchanges_endpoint(self, client: AsyncClient, server_health_check):
        response = await client.get("/")

        assert response.status_code == 200
        data = response.json()
        assert data["status"] == 200
        assert "exchanges" in data
        assert isinstance(data["exchanges"], list)
        assert "mercadobitcoin" in data["exchanges"]
        assert "coinbase" in data["exchanges"]


class TestMetricsEndpoints:
    @pytest.mark.asyncio
    async def test_metrics_exchanges_top_endpoint(self, client: AsyncClient, server_health_check):
        response = await client.get("/metrics/exchanges/top")

        assert response.status_code == 200
        data = response.json()
        assert data["status"] == 200
        assert "top_exchanges" in data
        assert isinstance(data["top_exchanges"], list)

    @pytest.mark.asyncio
    async def test_metrics_exchanges_top_with_limit_endpoint(self, client: AsyncClient, server_health_check):
        response = await client.get("/metrics/exchanges/top?limit=5")

        assert response.status_code == 200
        data = response.json()
        assert data["status"] == 200
        assert "top_exchanges" in data
        assert isinstance(data["top_exchanges"], list)
        assert len(data["top_exchanges"]) <= 5

    @pytest.mark.asyncio
    async def test_metrics_tickers_top_endpoint(self, client: AsyncClient, server_health_check):
        response = await client.get("/metrics/tickers/top")

        assert response.status_code == 200
        data = response.json()
        assert data["status"] == 200
        assert "top_tickers" in data
        assert isinstance(data["top_tickers"], list)

    @pytest.mark.asyncio
    async def test_metrics_tickers_top_with_limit_endpoint(self, client: AsyncClient, server_health_check):
        response = await client.get("/metrics/tickers/top?limit=3")

        assert response.status_code == 200
        data = response.json()
        assert data["status"] == 200
        assert "top_tickers" in data
        assert isinstance(data["top_tickers"], list)
        assert len(data["top_tickers"]) <= 3

    @pytest.mark.asyncio
    async def test_metrics_performance_endpoint(self, client: AsyncClient, server_health_check):
        response = await client.get("/metrics/performance")

        assert response.status_code == 200
        data = response.json()
        assert data["status"] == 200
        assert "performance" in data

    @pytest.mark.asyncio
    async def test_metrics_summary_endpoint(self, client: AsyncClient, server_health_check):
        response = await client.get("/metrics/summary")

        assert response.status_code == 200
        data = response.json()
        assert data["status"] == 200
        assert "summary" in data


class TestDocumentationEndpoints:
    @pytest.mark.asyncio
    async def test_api_documentation_available(self, client: AsyncClient, server_health_check):
        response = await client.get("/docs")

        assert response.status_code == 200


class TestSymbolsEndpoints:
    @pytest.mark.asyncio
    async def test_symbols_endpoint_missing_exchange(self, client: AsyncClient, server_health_check):
        response = await client.post("/symbols", json={})

        assert response.status_code == 422

    @pytest.mark.asyncio
    async def test_symbols_endpoint_valid_exchange(self, client: AsyncClient, server_health_check):
        response = await client.post("/symbols", json={"exchange": "coinbase"})

        assert response.status_code == 200
        data = response.json()
        assert data["status"] == 200

    @pytest.mark.asyncio
    async def test_symbols_endpoint_invalid_exchange(self, client: AsyncClient, server_health_check):
        response = await client.post("/symbols", json={"exchange": "invalid"})

        assert response.status_code == 200
        data = response.json()
        assert data["status"] == 404


class TestTickersEndpoints:
    @pytest.mark.asyncio
    async def test_tickers_endpoint_missing_params(self, client: AsyncClient, server_health_check):
        response = await client.post("/tickers", json={})

        assert response.status_code == 422

    @pytest.mark.asyncio
    async def test_tickers_endpoint_valid_request(self, client: AsyncClient, server_health_check):
        response = await client.post("/tickers", json={
            "exchange": "coinbase",
            "tickers": ["BTC-USD"]
        })

        assert response.status_code == 200
        data = response.json()
        assert data["status"] == 200

    @pytest.mark.asyncio
    async def test_tickers_endpoint_invalid_exchange(self, client: AsyncClient, server_health_check):
        response = await client.post("/tickers", json={
            "exchange": "invalid",
            "tickers": ["BTC-USD"]
        })

        assert response.status_code == 200
        data = response.json()
        assert data["status"] == 404

    @pytest.mark.asyncio
    async def test_tickers_endpoint_empty_tickers(self, client: AsyncClient, server_health_check):
        response = await client.post("/tickers", json={
            "exchange": "coinbase",
            "tickers": []
        })

        assert response.status_code == 422