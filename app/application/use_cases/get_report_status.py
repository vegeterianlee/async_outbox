from dataclasses import dataclass
from typing import Optional

from app.celery_app import celery_app


@dataclass
class GetReportStatusQuery:
    report_id: int


@dataclass
class ReportStatusDTO:
    id: int
    job_id: Optional[str]
    celery_status: Optional[str]
    result_path: Optional[str]
    error_message: Optional[str]


class GetReportStatusUseCase:
    def __init__(self, uow_factory):
        self._uow_factory = uow_factory

    async def execute(self, query: GetReportStatusQuery) -> ReportStatusDTO:
        async with self._uow_factory() as uow:
            report = await uow.reports.get(query.report_id)
            if not report:
                raise ValueError("Report not found")

            # job_id가 아직 없는 경우라면, outbox dispatcher가 queue에 넣지 할당하지 않은 상태를 의미
            if not report.job_id:
                celery_status: Optional[str] = "PENDING_DISPATCH"
            else:
                async_result = celery_app.AsyncResult(report.job_id)
                celery_status = async_result.status
                if celery_status == "PROGRESS":
                    meta = async_result.info or {}
                    progress = meta.get("progress")
                    celery_status = f"PROGRESS:{progress}%" if progress is not None else "PROGRESS"

            return ReportStatusDTO(
                id=report.id,
                job_id=report.job_id,
                celery_status=celery_status,
                result_path=report.result_path,
                error_message=report.error_message,
            )


