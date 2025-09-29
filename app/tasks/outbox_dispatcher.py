import logging
import asyncio

from app.celery_app import celery_app
from app.db.session import async_session_factory
from app.infrastructure.uow.sqlalchemy_uow import SqlAlchemyUnitOfWork
from app.tasks.report_tasks import generate_report


logger = logging.getLogger(__name__)

@celery_app.task(name="dispatch_outbox_events")
def dispatch_outbox_events() -> None:
    asyncio.run(_dispatch_events_async())


async def _dispatch_events_async() -> None:
    async with async_session_factory() as session:
        uow = SqlAlchemyUnitOfWork(session)
        pending = await uow.outbox.list_pending(limit=100)
        for event in pending:
            try:
                if event.event_type == "ReportRequested":
                    job = generate_report.delay(event.payload["report_id"], event.payload["params"])
                    await uow.reports.set_job_id(int(event.payload["report_id"]), job.id)
                await uow.outbox.mark_dispatched(event.id)
                await uow.commit()

            except Exception as e:
                logger.exception("Failed to dispatch outbox event %s", event.id)
                await uow.outbox.mark_failed(event.id, str(e))
                await uow.commit()


