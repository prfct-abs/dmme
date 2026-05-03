from celery.schedules import crontab
from app.workers.celery_app import celery_app

celery_app.conf.beat_schedule = {
    # Refresh expiring OAuth tokens every 6 hours
    "refresh-oauth-tokens": {
        "task":     "app.workers.maintenance_tasks.refresh_expiring_tokens",
        "schedule": crontab(minute=0, hour="*/6"),
    },
    # Reset daily DM counters in Redis at midnight UTC
    "reset-daily-counters": {
        "task":     "app.workers.maintenance_tasks.reset_daily_counters",
        "schedule": crontab(minute=0, hour=0),
    },
}
