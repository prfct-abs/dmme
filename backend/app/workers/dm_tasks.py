import logging
from celery import shared_task
from celery.utils.log import get_task_logger

logger = get_task_logger(__name__)


@shared_task(
    bind=True,
    name="app.workers.dm_tasks.send_dm",
    max_retries=3,
    default_retry_delay=60,    # Retry after 60s
    queue="dm_dispatch",
)
def send_dm(self, campaign_id: str, recipient_id: str, message: dict, platform: str, access_token: str):
    """
    Dispatch a single DM to a platform user.
    Retries up to 3 times on failure with exponential backoff.
    """
    try:
        logger.info(f"Sending DM | campaign={campaign_id} recipient={recipient_id} platform={platform}")

        if platform == "instagram":
            _send_instagram_dm(recipient_id, message, access_token)
        elif platform == "twitter":
            _send_twitter_dm(recipient_id, message, access_token)
        elif platform == "linkedin":
            _send_linkedin_dm(recipient_id, message, access_token)
        else:
            raise ValueError(f"Unknown platform: {platform}")

        # TODO: update DmEvent status to 'sent' in DB (use sync sqlalchemy or httpx to call internal API)
        logger.info(f"DM sent successfully | recipient={recipient_id}")

    except Exception as exc:
        logger.error(f"DM failed | recipient={recipient_id} error={exc}")
        raise self.retry(exc=exc, countdown=60 * (self.request.retries + 1))


# ── Platform dispatch helpers ───────────────────────────────────────────────

def _send_instagram_dm(recipient_id: str, message: dict, access_token: str):
    import httpx
    resp = httpx.post(
        f"https://graph.facebook.com/v19.0/me/messages",
        params={"access_token": access_token},
        json={
            "recipient": {"id": recipient_id},
            "message": {"text": message.get("body", "")},
        },
        timeout=10,
    )
    resp.raise_for_status()


def _send_twitter_dm(recipient_id: str, message: dict, access_token: str):
    import httpx
    resp = httpx.post(
        "https://api.twitter.com/2/dm_conversations/with/:participant_id/messages",
        headers={"Authorization": f"Bearer {access_token}"},
        json={"text": message.get("body", "")},
        timeout=10,
    )
    resp.raise_for_status()


def _send_linkedin_dm(recipient_id: str, message: dict, access_token: str):
    # LinkedIn messaging API placeholder
    pass
