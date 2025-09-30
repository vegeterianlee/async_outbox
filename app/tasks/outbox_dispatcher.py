from app.celery_app import celery_app
from app.db.worker_session import get_session
from app.infrastructure.uow.sqlalchemy_uow import SqlAlchemyUnitOfWork
from app.tasks.report_tasks import generate_report
from app.common.async_runner import run_in_single_loop

@celery_app.task(name="dispatch_outbox_events")
def dispatch_outbox_events() -> None:
    run_in_single_loop(_dispatch_events_async())


async def _dispatch_events_async() -> None:
    async with get_session() as session:
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
                await uow.outbox.mark_failed(event.id, str(e))
                await uow.commit()



