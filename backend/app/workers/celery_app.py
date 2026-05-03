from celery import Celery
from app.config import settings

celery_app = Celery(
    "autodm",
    broker=settings.REDIS_URL,
    backend=settings.REDIS_URL,
    include=["app.workers.dm_tasks"],
)

celery_app.conf.update(
    task_serializer="json",
    result_serializer="json",
    accept_content=["json"],
    timezone="UTC",
    enable_utc=True,
    task_acks_late=True,            # Only ack after task completes (safer)
    task_reject_on_worker_lost=True,
    worker_prefetch_multiplier=1,   # One task at a time per worker (rate limiting)
    task_routes={
        "app.workers.dm_tasks.send_dm": {"queue": "dm_dispatch"},
    },
)
