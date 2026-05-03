import hashlib
import hmac

from sqlalchemy.ext.asyncio import AsyncSession

from app.config import settings
from app.services.campaign_service import CampaignService


class WebhookService:
    def __init__(self, db: AsyncSession):
        self.db           = db
        self.campaign_svc = CampaignService(db)

    # ── Instagram ────────────────────────────────────────────────────────────
    async def handle_instagram(self, payload: dict) -> None:
        """
        Instagram sends batched entries. Each entry can have changes:
        - messaging (DM received)
        - comments (post comment created)
        """
        for entry in payload.get("entry", []):
            for change in entry.get("changes", []):
                field = change.get("field")
                value = change.get("value", {})

                if field == "comments":
                    await self._handle_ig_comment(value)
                elif field == "messages":
                    await self._handle_ig_dm(value)

    async def _handle_ig_comment(self, value: dict) -> None:
        comment_text = value.get("text", "").upper()
        sender_id    = value.get("from", {}).get("id")
        if not sender_id:
            return

        await self.campaign_svc.evaluate_trigger({
            "platform":  "instagram",
            "type":      "comment_keyword",
            "keyword":   comment_text,
            "sender_id": sender_id,
        })

    async def _handle_ig_dm(self, value: dict) -> None:
        messages = value.get("messages", [])
        for msg in messages:
            text      = msg.get("text", {}).get("body", "").upper()
            sender_id = msg.get("sender", {}).get("id")
            if sender_id:
                await self.campaign_svc.evaluate_trigger({
                    "platform":  "instagram",
                    "type":      "dm_keyword",
                    "keyword":   text,
                    "sender_id": sender_id,
                })

    # ── X (Twitter) ──────────────────────────────────────────────────────────
    async def handle_twitter(self, payload: dict) -> None:
        events = payload.get("direct_message_events", [])
        for event in events:
            if event.get("type") != "message_create":
                continue
            msg_data  = event.get("message_create", {})
            sender_id = msg_data.get("sender_id")
            text      = msg_data.get("message_data", {}).get("text", "").upper()
            if sender_id:
                await self.campaign_svc.evaluate_trigger({
                    "platform":  "twitter",
                    "type":      "dm_keyword",
                    "keyword":   text,
                    "sender_id": sender_id,
                })

    # ── HMAC verification helpers ─────────────────────────────────────────────
    @staticmethod
    def verify_instagram_hmac(body: bytes, signature_header: str) -> bool:
        if not signature_header or not signature_header.startswith("sha256="):
            return False
        expected = "sha256=" + hmac.new(
            settings.INSTAGRAM_APP_SECRET.encode(), body, hashlib.sha256
        ).hexdigest()
        return hmac.compare_digest(expected, signature_header)
