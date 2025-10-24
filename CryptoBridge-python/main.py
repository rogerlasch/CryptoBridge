import asyncio
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.infrastructure.database.connection import engine, Base
from src.infrastructure.database import models  # Import models to register them
from src.presentation.api.routers.bridge_router import router as bridge_router
from src.presentation.api.routers.metrics_router import router as metrics_router
from src.presentation.api.middleware import MetricsMiddleware


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    print("CryptoBridge Python API iniciada na porta 3000")
    print("Banco de dados SQLite inicializado automaticamente")
    print("Endpoints disponíveis:")
    print("  GET  / - Lista exchanges disponíveis")
    print("  POST /symbols - Lista símbolos (body: {exchange})")
    print("  POST /tickers - Busca preços (body: {exchange, tickers[]})")
    print("  GET  /metrics/* - Endpoints de métricas")
    print("  GET  /docs - Documentação Swagger")

    yield


app = FastAPI(
    title="CryptoBridge API",
    description="Agregador de preços de criptomoedas",
    version="1.0.0",
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_middleware(MetricsMiddleware)

app.include_router(bridge_router)
app.include_router(metrics_router, prefix="/metrics")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=3000)