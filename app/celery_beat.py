from datetime import timedelta
from app.celery_app import celery_app

celery_app.conf.beat_schedule = {
    "dispatch-outbox-every-2s": {
        "task": "dispatch_outbox_events",
        "schedule": timedelta(seconds=2),
    }
}


