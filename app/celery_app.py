from celery import Celery
from app.core.config import settings

celery_app = Celery(
    "async_outbox",
    broker=settings.REDIS_URL,
    backend=settings.REDIS_URL,
)

celery_app.conf.update(
    task_serializer="json",
    result_serializer="json",
    accept_content=["json"],
    timezone="UTC",
    enable_utc=True,
    imports=(
        "app.tasks.outbox_dispatcher",
        "app.celery_beat",
    ),
)

celery_app.autodiscover_tasks(["app.tasks"]) 


