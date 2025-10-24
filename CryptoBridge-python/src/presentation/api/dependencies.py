from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from ...infrastructure.database.connection import get_db
from ...infrastructure.repositories.exchange_repository_impl import ExchangeRepositoryImpl
from ...infrastructure.repositories.metrics_repository_impl import MetricsRepositoryImpl
from ...application.services.bridge_service import BridgeService
from ...application.services.metrics_service import MetricsService


def get_exchange_repository() -> ExchangeRepositoryImpl:
    return ExchangeRepositoryImpl()


async def get_metrics_repository(db: AsyncSession = Depends(get_db)) -> MetricsRepositoryImpl:
    return MetricsRepositoryImpl(db)


async def get_bridge_service(
    exchange_repo: ExchangeRepositoryImpl = Depends(get_exchange_repository),
    metrics_repo: MetricsRepositoryImpl = Depends(get_metrics_repository)
) -> BridgeService:
    return BridgeService(exchange_repo, metrics_repo)


async def get_metrics_service(
    metrics_repo: MetricsRepositoryImpl = Depends(get_metrics_repository)
) -> MetricsService:
    return MetricsService(metrics_repo)