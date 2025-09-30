from dataclasses import dataclass
from app.schemas.metrics import SimpleTaskMetricsOut


@dataclass
class SimpleTaskMetricsDTO:
    total_requests: int
    queued_now: int
    processing_now: int
    completed_success: int


class GetTaskMetricsUseCase:
    def __init__(self, uow_factory, worker_probe, broker_probe):
        self._uow_factory = uow_factory
        self._worker = worker_probe
        self._broker = broker_probe

    async def execute(self) -> SimpleTaskMetricsOut:
        async with self._uow_factory() as uow:
            total_requests = await uow.metrics.count_total_requests()
            completed_success = await uow.metrics.count_completed_success()
            completed_failed = total_requests - completed_success

            # 현재 시점(워커/브로커 스냅샷)
            worker_active, worker_reserved, worker_scheduled = await self._worker.get_counts()
            broker_queued = await self._broker.count_queued()
            outbox_pending = await uow.metrics.count_outbox_pending()

            queued_now = outbox_pending + broker_queued + worker_reserved + worker_scheduled
            processing_now = worker_active

            dto = SimpleTaskMetricsDTO(
                total_requests=total_requests,
                queued_now=queued_now,
                processing_now=processing_now,
                completed_success=completed_success,

            )
            return SimpleTaskMetricsOut(
                total_requests=dto.total_requests,
                queued_now=dto.queued_now,
                processing_now=dto.processing_now,
                completed_success=dto.completed_success,
            )