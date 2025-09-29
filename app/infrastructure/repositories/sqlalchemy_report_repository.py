from typing import Optional

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update

from app.domain.entities.report_request import ReportRequestEntity
from app.domain.repositories.report_repository import ReportRepository
from app.models.report import ReportRequest


def _to_entity(row: ReportRequest) -> ReportRequestEntity:
    return ReportRequestEntity(
        id=row.id,
        requester_email=row.requester_email,
        params=row.params,
        job_id=row.job_id,
        result_path=row.result_path,
        error_message=row.error_message,
        created_at=row.created_at,
        updated_at=row.updated_at,
    )


class SqlAlchemyReportRepository(ReportRepository):
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def add(self, report: ReportRequestEntity) -> ReportRequestEntity:
        row = ReportRequest(requester_email=report.requester_email, params=report.params)
        self._session.add(row)
        await self._session.flush()
        return _to_entity(row)

    async def get(self, report_id: int) -> Optional[ReportRequestEntity]:
        row = await self._session.get(ReportRequest, report_id)
        return _to_entity(row) if row else None

    async def set_job_id(self, report_id: int, job_id: str) -> None:
        await self._session.execute(
            update(ReportRequest).where(ReportRequest.id == report_id).values(job_id=job_id)
        )

    async def set_result(self, report_id: int, result_path: str) -> None:
        await self._session.execute(
            update(ReportRequest).where(ReportRequest.id == report_id).values(result_path=result_path, error_message=None)
        )

    async def set_error(self, report_id: int, error_message: str) -> None:
        await self._session.execute(
            update(ReportRequest).where(ReportRequest.id == report_id).values(error_message=error_message)
        )


