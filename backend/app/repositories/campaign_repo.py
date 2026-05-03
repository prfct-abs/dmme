from uuid import UUID

from sqlalchemy import select, and_
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.campaign import Campaign, CampaignStatus
from app.schemas.campaign import CampaignCreate, CampaignUpdate


class CampaignRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def list_by_user(self, user_id: UUID, page: int = 1, page_size: int = 20) -> list[Campaign]:
        offset = (page - 1) * page_size
        result = await self.db.execute(
            select(Campaign)
            .where(Campaign.user_id == user_id)
            .order_by(Campaign.created_at.desc())
            .offset(offset).limit(page_size)
        )
        return list(result.scalars().all())

    async def get(self, campaign_id: UUID, user_id: UUID) -> Campaign | None:
        result = await self.db.execute(
            select(Campaign).where(and_(Campaign.id == campaign_id, Campaign.user_id == user_id))
        )
        return result.scalar_one_or_none()

    async def create(self, user_id: UUID, payload: CampaignCreate) -> Campaign:
        camp = Campaign(
            user_id=user_id,
            social_account_id=payload.social_account_id,
            name=payload.name,
            platform=payload.platform,
            trigger_config=payload.trigger_config.model_dump(),
            message_template=payload.message_template.model_dump(),
            daily_limit=payload.daily_limit,
        )
        self.db.add(camp)
        await self.db.commit()
        await self.db.refresh(camp)
        return camp

    async def update(self, campaign_id: UUID, user_id: UUID, payload: CampaignUpdate) -> Campaign:
        camp = await self.get(campaign_id, user_id)
        if not camp:
            raise ValueError("Not found")
        for field, value in payload.model_dump(exclude_none=True).items():
            if isinstance(value, dict):
                setattr(camp, field, value)
            else:
                setattr(camp, field, value)
        await self.db.commit()
        await self.db.refresh(camp)
        return camp

    async def set_status(self, campaign_id: UUID, status: CampaignStatus) -> Campaign:
        result = await self.db.execute(select(Campaign).where(Campaign.id == campaign_id))
        camp = result.scalar_one()
        camp.status = status
        await self.db.commit()
        await self.db.refresh(camp)
        return camp

    async def delete(self, campaign_id: UUID, user_id: UUID) -> None:
        camp = await self.get(campaign_id, user_id)
        if camp:
            await self.db.delete(camp)
            await self.db.commit()

    async def find_matching(self, platform: str, trigger_type: str, keyword: str) -> list[Campaign]:
        """Find active campaigns matching a platform + trigger type + keyword."""
        result = await self.db.execute(
            select(Campaign).where(
                and_(
                    Campaign.platform == platform,
                    Campaign.status == CampaignStatus.active,
                )
            )
        )
        campaigns = list(result.scalars().all())

        # Filter by trigger type and keyword in Python (JSONB could do this in SQL too)
        matched = []
        for camp in campaigns:
            tc = camp.trigger_config
            if tc.get("type") != trigger_type:
                continue
            kws = [k.upper() for k in tc.get("keywords", [])]
            if trigger_type in ("comment_keyword", "dm_keyword") and kws and keyword not in kws:
                continue
            matched.append(camp)
        return matched
