from datetime import date
from uuid import UUID

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.campaign import Campaign
from app.models.dm_event import DmEvent, DmEventStatus


class AnalyticsService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_metrics(
        self,
        user_id: UUID,
        campaign_id: str | None = None,
        from_date: str | None = None,
        to_date:   str | None = None,
    ) -> dict:
        # Base query scoped to user's campaigns
        stmt = (
            select(DmEvent)
            .join(Campaign, DmEvent.campaign_id == Campaign.id)
            .where(Campaign.user_id == user_id)
        )
        if campaign_id:
            stmt = stmt.where(DmEvent.campaign_id == UUID(campaign_id))
        if from_date:
            stmt = stmt.where(DmEvent.sent_at >= from_date)
        if to_date:
            stmt = stmt.where(DmEvent.sent_at <= to_date)

        result = await self.db.execute(stmt)
        events: list[DmEvent] = list(result.scalars().all())

        total_sent    = len(events)
        total_replied = sum(1 for e in events if e.status == DmEventStatus.replied)
        total_failed  = sum(1 for e in events if e.status == DmEventStatus.failed)

        # DMs sent per day
        day_counts: dict[str, int] = {}
        for e in events:
            if e.sent_at:
                day = str(e.sent_at)[:10]
                day_counts[day] = day_counts.get(day, 0) + 1

        sent_by_day = [{"date": k, "count": v} for k, v in sorted(day_counts.items())]

        return {
            "total_sent":    total_sent,
            "total_replied": total_replied,
            "reply_rate":    round(total_replied / total_sent * 100, 1) if total_sent else 0,
            "failure_rate":  round(total_failed  / total_sent * 100, 1) if total_sent else 0,
            "sent_by_day":   sent_by_day,
        }

    async def get_events(
        self, user_id: UUID, campaign_id: str | None = None, limit: int = 50
    ) -> list[DmEvent]:
        stmt = (
            select(DmEvent)
            .join(Campaign, DmEvent.campaign_id == Campaign.id)
            .where(Campaign.user_id == user_id)
            .order_by(DmEvent.sent_at.desc())
            .limit(limit)
        )
        if campaign_id:
            stmt = stmt.where(DmEvent.campaign_id == UUID(campaign_id))

        result = await self.db.execute(stmt)
        return list(result.scalars().all())
