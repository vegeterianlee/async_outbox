from contextlib import asynccontextmanager

from fastapi import FastAPI
from app.api.routes.reports import router as reports_router
from app.common.exceptions.exception_handler import global_exception_handler
from app.core.config import settings
from app.db.session import async_engine
from app.db.base import Base
from app import models
from app.common.api_response import api_response

def create_app() -> FastAPI:
    @asynccontextmanager
    async def lifespan(app: FastAPI):
        async with async_engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
        try:
            yield
        finally:
            await async_engine.dispose()

    app = FastAPI(title="Async Outbox API", version="0.1.0", lifespan=lifespan)
    @app.get("/health")
    async def health_check():
        return api_response({"status": "ok", "environment": settings.ENVIRONMENT})

    app.include_router(reports_router, prefix="/reports", tags=["reports"])

    # 전역 에러 핸들러 등록
    global_exception_handler(app)
    return app

app = create_app()