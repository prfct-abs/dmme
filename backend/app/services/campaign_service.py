from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from app.models.campaign import Campaign, CampaignStatus
from app.repositories.campaign_repo import CampaignRepository
from app.schemas.campaign import CampaignCreate, CampaignUpdate
from app.workers.dm_tasks import send_dm


class CampaignService:
    def __init__(self, db: AsyncSession):
        self.db   = db
        self.repo = CampaignRepository(db)

    async def list_for_user(self, user_id: UUID, page: int = 1, page_size: int = 20) -> list[Campaign]:
        return await self.repo.list_by_user(user_id, page=page, page_size=page_size)

    async def get(self, campaign_id: UUID, user_id: UUID) -> Campaign | None:
        return await self.repo.get(campaign_id, user_id)

    async def create(self, user_id: UUID, payload: CampaignCreate) -> Campaign:
        return await self.repo.create(user_id, payload)

    async def update(self, campaign_id: UUID, user_id: UUID, payload: CampaignUpdate) -> Campaign:
        return await self.repo.update(campaign_id, user_id, payload)

    async def toggle(self, campaign_id: UUID, user_id: UUID) -> Campaign:
        camp = await self.repo.get(campaign_id, user_id)
        if not camp:
            raise ValueError("Campaign not found")
        new_status = CampaignStatus.paused if camp.status == CampaignStatus.active else CampaignStatus.active
        return await self.repo.set_status(campaign_id, new_status)

    async def delete(self, campaign_id: UUID, user_id: UUID) -> None:
        await self.repo.delete(campaign_id, user_id)

    # ── Trigger evaluation ───────────────────────────────────────────────────
    async def evaluate_trigger(self, event: dict) -> None:
        """
        Called by WebhookService when a platform event arrives.
        Matches event against active campaigns and enqueues DM jobs.
        """
        import redis.asyncio as aioredis
        from app.config import settings

        platform   = event.get("platform")
        event_type = event.get("type")       # comment_keyword | story_reply | new_follower
        keyword    = event.get("keyword", "").upper()
        sender_id  = event.get("sender_id")

        # Find matching active campaigns
        campaigns = await self.repo.find_matching(
            platform=platform, trigger_type=event_type, keyword=keyword
        )

        redis = aioredis.from_url(settings.REDIS_URL, decode_responses=True)

        for camp in campaigns:
            # Per-user rate limit: skip if already DM'd today
            rate_key = f"dm_rate:{camp.id}:{sender_id}"
            already_sent = await redis.get(rate_key)
            if already_sent:
                continue

            # Enqueue Celery task
            send_dm.apply_async(
                kwargs={
                    "campaign_id":  str(camp.id),
                    "recipient_id": sender_id,
                    "message":      camp.message_template,
                    "platform":     camp.platform,
                    "access_token": "",   # Fetched inside task from DB
                },
                queue="dm_dispatch",
            )

            # Mark as sent for today (TTL = 24h)
            await redis.setex(rate_key, 86400, "1")

        await redis.aclose()
