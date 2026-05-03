import httpx
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.dm_event import DmEvent, DmEventStatus
from app.repositories.event_repo import EventRepository


class DmService:
    def __init__(self, db: AsyncSession):
        self.db   = db
        self.repo = EventRepository(db)

    # ── Message formatting ───────────────────────────────────────────────────
    @staticmethod
    def render_message(template: dict, context: dict) -> str:
        """Replace {{variable}} placeholders with context values."""
        body = template.get("body", "")
        for key, value in context.items():
            body = body.replace(f"{{{{{key}}}}}", str(value))
        return body

    # ── Platform dispatch ────────────────────────────────────────────────────
    async def dispatch(
        self,
        platform: str,
        recipient_id: str,
        message: dict,
        access_token: str,
        campaign_id: str,
        context: dict | None = None,
    ) -> DmEvent:
        """Format, send, and log a DM. Returns the created DmEvent."""
        rendered_body = self.render_message(message, context or {})
        rendered_msg  = {**message, "body": rendered_body}

        success = False
        try:
            if platform == "instagram":
                await self._send_instagram(recipient_id, rendered_body, access_token)
            elif platform == "twitter":
                await self._send_twitter(recipient_id, rendered_body, access_token)
            elif platform == "linkedin":
                await self._send_linkedin(recipient_id, rendered_body, access_token)
            success = True
        except Exception:
            pass

        status = DmEventStatus.sent if success else DmEventStatus.failed
        return await self.repo.create_event(
            campaign_id=campaign_id,
            recipient_platform_id=recipient_id,
            status=status,
            message_snapshot=rendered_msg,
        )

    # ── Instagram Graph API ──────────────────────────────────────────────────
    @staticmethod
    async def _send_instagram(recipient_id: str, body: str, token: str):
        async with httpx.AsyncClient() as client:
            resp = await client.post(
                "https://graph.facebook.com/v19.0/me/messages",
                params={"access_token": token},
                json={"recipient": {"id": recipient_id}, "message": {"text": body}},
                timeout=10,
            )
            resp.raise_for_status()

    # ── X (Twitter) API v2 ───────────────────────────────────────────────────
    @staticmethod
    async def _send_twitter(recipient_id: str, body: str, token: str):
        async with httpx.AsyncClient() as client:
            resp = await client.post(
                f"https://api.twitter.com/2/dm_conversations/with/{recipient_id}/messages",
                headers={"Authorization": f"Bearer {token}"},
                json={"text": body},
                timeout=10,
            )
            resp.raise_for_status()

    # ── LinkedIn ─────────────────────────────────────────────────────────────
    @staticmethod
    async def _send_linkedin(recipient_id: str, body: str, token: str):
        async with httpx.AsyncClient() as client:
            resp = await client.post(
                "https://api.linkedin.com/v2/messages",
                headers={"Authorization": f"Bearer {token}"},
                json={"recipients": [{"person": {"$URN": f"urn:li:person:{recipient_id}"}}], "body": body},
                timeout=10,
            )
            resp.raise_for_status()
