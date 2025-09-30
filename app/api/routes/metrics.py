from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.common.api_response import api_response, ApiResponse
from app.core.config import settings
from app.db.session import get_async_session
from app.application.use_cases.get_task_metrics import GetTaskMetricsUseCase
from app.infrastructure.probe.celery_worker_probe import CeleryWorkerProbe
from app.infrastructure.probe.redis_broker_probe import RedisBrokerProbe
from app.infrastructure.uow.sqlalchemy_uow import SqlAlchemyUnitOfWork
from app.schemas.metrics import SimpleTaskMetricsOut

router = APIRouter()


@router.get("/tasks", response_model=ApiResponse[SimpleTaskMetricsOut])
async def get_task_metrics(session: AsyncSession = Depends(get_async_session)):
    worker_probe = CeleryWorkerProbe()
    broker_probe = RedisBrokerProbe(settings.REDIS_URL)
    # lambda: 매 실행 시점마다 새 인스턴스를 생성하는 팩토리 역할 수행
    use_case = GetTaskMetricsUseCase(
        lambda: SqlAlchemyUnitOfWork(session),
        worker_probe,
        broker_probe
    )
    out = await use_case.execute()
    return api_response(data=out)


