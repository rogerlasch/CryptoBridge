import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def testGetExchangesEndpoint(client: AsyncClient):
    """Testa o endpoint de listagem de exchanges"""
    response = await client.get("/")

    assert response.status_code == 200
    data = response.json()
    assert data["status"] == 200
    assert "exchanges" in data
    assert isinstance(data["exchanges"], list)
    assert "mercadobitcoin" in data["exchanges"]
    assert "coinbase" in data["exchanges"]


@pytest.mark.asyncio
async def testMetricsExchangesTopEndpoint(client: AsyncClient):
    """Testa o endpoint de top exchanges nas métricas"""
    response = await client.get("/metrics/exchanges/top")

    assert response.status_code == 200
    data = response.json()
    assert data["status"] == 200
    assert "top_exchanges" in data


@pytest.mark.asyncio
async def testMetricsExchangesTopWithLimitEndpoint(client: AsyncClient):
    """Testa o endpoint de top exchanges com limite"""
    response = await client.get("/metrics/exchanges/top?limit=5")

    assert response.status_code == 200
    data = response.json()
    assert data["status"] == 200
    assert "top_exchanges" in data


@pytest.mark.asyncio
async def testMetricsTickersTopEndpoint(client: AsyncClient):
    """Testa o endpoint de top tickers nas métricas"""
    response = await client.get("/metrics/tickers/top")

    assert response.status_code == 200
    data = response.json()
    assert data["status"] == 200
    assert "top_tickers" in data


@pytest.mark.asyncio
async def testMetricsTickersTopWithLimitEndpoint(client: AsyncClient):
    """Testa o endpoint de top tickers com limite"""
    response = await client.get("/metrics/tickers/top?limit=3")

    assert response.status_code == 200
    data = response.json()
    assert data["status"] == 200
    assert "top_tickers" in data


@pytest.mark.asyncio
async def testMetricsPerformanceEndpoint(client: AsyncClient):
    """Testa o endpoint de métricas de performance"""
    response = await client.get("/metrics/performance")

    assert response.status_code == 200
    data = response.json()
    assert data["status"] == 200
    assert "performance" in data


@pytest.mark.asyncio
async def testMetricsSummaryEndpoint(client: AsyncClient):
    """Testa o endpoint de resumo das métricas"""
    response = await client.get("/metrics/summary")

    assert response.status_code == 200
    data = response.json()
    assert data["status"] == 200
    assert "summary" in data


@pytest.mark.asyncio
async def testApiDocumentationAvailable(client: AsyncClient):
    """Testa se a documentação da API está disponível"""
    response = await client.get("/docs")
    assert response.status_code == 200
    assert "swagger" in response.text.lower()

    response = await client.get("/openapi.json")
    assert response.status_code == 200
    data = response.json()
    assert "openapi" in data
    assert "info" in data


@pytest.mark.asyncio
async def testSymbolsEndpointMissingExchange(client: AsyncClient):
    """Testa o endpoint de símbolos sem parâmetro exchange"""
    response = await client.post("/symbols", json={})

    assert response.status_code == 422  # Validation error


@pytest.mark.asyncio
async def testSymbolsEndpointValidExchange(client: AsyncClient):
    """Testa o endpoint de símbolos com exchange válida"""
    response = await client.post("/symbols", json={"exchange": "coinbase"})

    assert response.status_code == 200
    data = response.json()
    assert data["status"] == 200
    assert "symbols" in data


@pytest.mark.asyncio
async def testSymbolsEndpointInvalidExchange(client: AsyncClient):
    """Testa o endpoint de símbolos com exchange inválida"""
    response = await client.post("/symbols", json={"exchange": "invalid"})

    assert response.status_code == 200
    data = response.json()
    assert data["status"] == 404


@pytest.mark.asyncio
async def testTickersEndpointMissingParams(client: AsyncClient):
    """Testa o endpoint de tickers sem parâmetros"""
    response = await client.post("/tickers", json={})

    assert response.status_code == 422  # Validation error


@pytest.mark.asyncio
async def testTickersEndpointValidRequest(client: AsyncClient):
    """Testa o endpoint de tickers com requisição válida"""
    response = await client.post("/tickers", json={
        "exchange": "coinbase",
        "tickers": ["BTC-USD"]
    })

    assert response.status_code == 200
    data = response.json()
    assert data["status"] == 200
    assert "tickers" in data


@pytest.mark.asyncio
async def testTickersEndpointInvalidExchange(client: AsyncClient):
    """Testa o endpoint de tickers com exchange inválida"""
    response = await client.post("/tickers", json={
        "exchange": "invalid",
        "tickers": ["BTC-USD"]
    })

    assert response.status_code == 200
    data = response.json()
    assert data["status"] == 404


@pytest.mark.asyncio
async def testTickersEndpointEmptyTickers(client: AsyncClient):
    """Testa o endpoint de tickers com lista vazia"""
    response = await client.post("/tickers", json={
        "exchange": "coinbase",
        "tickers": []
    })

    assert response.status_code == 422  # Validation error (min_items=1)