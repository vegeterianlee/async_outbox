from sqlalchemy import select, func, or_
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.report import ReportRequest
from app.models.outbox import OutboxEvent

class SqlAlchemyReportMetricsRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._s = session

    async def count_total_requests(self) -> int:
        v = await self._s.scalar(select(func.count()).select_from(ReportRequest))
        return int(v or 0)

    async def count_completed_success(self) -> int:
        v = await self._s.scalar(
            select(func.count()).select_from(ReportRequest)
            .where(ReportRequest.result_path.isnot(None))
        )
        return int(v or 0)

    async def count_outbox_pending(self) -> int:
        v = await self._s.scalar(
            select(func.count()).select_from(OutboxEvent)
            .where(OutboxEvent.status == "pending")
        )
        return int(v or 0)