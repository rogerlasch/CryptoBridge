import time
from fastapi import Request, Response
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware

from ...infrastructure.database.connection import AsyncSessionLocal
from ...infrastructure.repositories.metrics_repository_impl import MetricsRepositoryImpl
from ...application.services.metrics_service import MetricsService


class MetricsMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        start_time = time.time()

        response = await call_next(request)

        process_time = (time.time() - start_time) * 1000

        try:
            async with AsyncSessionLocal() as db:
                metrics_repo = MetricsRepositoryImpl(db)
                await metrics_repo.record_api_call(
                    endpoint=str(request.url.path),
                    method=request.method,
                    status_code=response.status_code,
                    response_time_ms=process_time
                )
        except Exception as e:
            print(f"Erro ao registrar métricas: {e}")

        return response