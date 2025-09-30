from typing import Protocol

from app.domain.repositories.metrics_repository import ReportMetricsRepository
from app.domain.repositories.outbox_repository import OutboxRepository
from app.domain.repositories.report_repository import ReportRepository


class UnitOfWork(Protocol):
    outbox: OutboxRepository
    reports: ReportRepository
    metrics: ReportMetricsRepository

    async def __aenter__(self) -> "UnitOfWork": ...

    async def __aexit__(self, exc_type, exc, tb) -> None: ...

    async def commit(self) -> None: ...

    async def rollback(self) -> None: ...


