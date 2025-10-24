from fastapi import APIRouter, Depends, Query
from ...schemas.metrics_schemas import (
    TopExchangesResponse, TopTickersResponse,
    PerformanceResponse, SummaryResponse
)
from ..dependencies import get_metrics_service
from ....application.services.metrics_service import MetricsService

router = APIRouter()


@router.get("/exchanges/top", response_model=TopExchangesResponse)
async def get_top_exchanges(
    limit: int = Query(10, ge=1, le=50, description="Número de exchanges no ranking"),
    metrics_service: MetricsService = Depends(get_metrics_service)
):
    try:
        result = await metrics_service.get_top_exchanges(limit)
        return result
    except Exception as e:
        print(f"Erro detalhado ao buscar top exchanges: {str(e)}")
        return {
            "status": 500,
            "msg": "Erro interno do servidor."
        }


@router.get("/tickers/top", response_model=TopTickersResponse)
async def get_top_tickers(
    limit: int = Query(10, ge=1, le=50, description="Número de tickers no ranking"),
    metrics_service: MetricsService = Depends(get_metrics_service)
):
    try:
        result = await metrics_service.get_top_tickers(limit)
        return result
    except Exception as e:
        print(f"Erro detalhado ao buscar top tickers: {str(e)}")
        return {
            "status": 500,
            "msg": "Erro interno do servidor."
        }


@router.get("/performance", response_model=PerformanceResponse)
async def get_performance_metrics(
    metrics_service: MetricsService = Depends(get_metrics_service)
):
    try:
        result = await metrics_service.get_performance_metrics()
        return result
    except Exception as e:
        print(f"Erro detalhado ao buscar métricas de performance: {str(e)}")
        return {
            "status": 500,
            "msg": "Erro interno do servidor."
        }


@router.get("/summary", response_model=SummaryResponse)
async def get_metrics_summary(
    metrics_service: MetricsService = Depends(get_metrics_service)
):
    try:
        result = await metrics_service.get_summary()
        return result
    except Exception as e:
        print(f"Erro detalhado ao buscar resumo de métricas: {str(e)}")
        return {
            "status": 500,
            "msg": "Erro interno do servidor."
        }