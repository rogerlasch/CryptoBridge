from fastapi import APIRouter, Depends, HTTPException
from typing import Union
from ...schemas.bridge_schemas import (
    TickerRequest, SymbolRequest, TickersResponse,
    SymbolsResponse, ExchangesResponse, ErrorResponse
)
from ..dependencies import get_bridge_service
from ....application.services.bridge_service import BridgeService

router = APIRouter()


@router.get("/", response_model=ExchangesResponse)
async def get_exchanges(
    bridge_service: BridgeService = Depends(get_bridge_service)
):
    try:
        result = await bridge_service.get_exchanges()
        return result
    except Exception as e:
        print(f"Erro detalhado ao buscar exchanges: {str(e)}")
        return {
            "status": 500,
            "msg": "Erro interno do servidor."
        }


@router.post("/symbols", response_model=Union[SymbolsResponse, ErrorResponse])
async def get_symbols(
    request: SymbolRequest,
    bridge_service: BridgeService = Depends(get_bridge_service)
):
    try:
        result = await bridge_service.get_symbols(request.exchange)
        return result
    except Exception as e:
        print(f"Erro detalhado ao buscar símbolos: {str(e)}")
        return {
            "status": 500,
            "msg": "Erro interno do servidor."
        }


@router.post("/tickers", response_model=Union[TickersResponse, ErrorResponse])
async def get_tickers(
    request: TickerRequest,
    bridge_service: BridgeService = Depends(get_bridge_service)
):
    try:
        result = await bridge_service.get_tickers(request.exchange, request.tickers)
        return result
    except Exception as e:
        print(f"Erro detalhado ao buscar tickers: {str(e)}")
        return {
            "status": 500,
            "msg": "Erro interno do servidor."
        }