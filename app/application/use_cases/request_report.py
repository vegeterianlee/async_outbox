from dataclasses import dataclass
from datetime import datetime

from app.domain.entities.report_request import ReportRequestEntity
from app.domain.entities.outbox_event import OutboxEventEntity, OutboxStatus
from app.schemas.report import ReportParams, ReportRequestOut


@dataclass
class RequestReportCommand:
    requester_email: str
    params: ReportParams


class RequestReportUseCase:
    def __init__(self, uow_factory):
        self._uow_factory = uow_factory

    async def execute(self, cmd: RequestReportCommand) -> ReportRequestOut:
        async with self._uow_factory() as uow:
            params_dict = cmd.params.model_dump()
            report = ReportRequestEntity(
                id=None,
                requester_email=cmd.requester_email,
                params=params_dict,
                job_id=None,
                result_path=None,
                error_message=None,
                created_at=datetime.utcnow(),
                updated_at=datetime.utcnow(),
            )
            report = await uow.reports.add(report)

            # Outbox event
            # Dispatcher가 celery에 작업을 위임하고 job_id 설정해줌
            event = OutboxEventEntity(
                id=None,
                aggregate_type="report",
                aggregate_id=str(report.id),
                event_type="ReportRequested",
                payload={
                    "report_id": report.id,
                    "requester_email": report.requester_email,
                    "params": report.params,
                },
                status=OutboxStatus.pending,
                attempts=0,
                last_error=None,
                created_at=datetime.utcnow(),
                dispatched_at=None,
            )
            await uow.outbox.add(event)
            await uow.commit()

            report_status = ReportRequestOut(
                id=report.id,
                job_id=report.job_id,
                params=report.params,
                result_path=report.result_path,
                created_at=report.created_at,
            )
            return report_status


