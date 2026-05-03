from uuid import UUID
from datetime import datetime, timezone

from sqlalchemy import select, and_
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.dm_event import DmEvent, DmEventStatus


class EventRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create_event(
        self,
        campaign_id: str,
        recipient_platform_id: str,
        status: DmEventStatus,
        message_snapshot: dict,
        recipient_username: str | None = None,
    ) -> DmEvent:
        event = DmEvent(
            campaign_id=UUID(campaign_id),
            recipient_platform_id=recipient_platform_id,
            recipient_username=recipient_username,
            status=status,
            message_snapshot=message_snapshot,
            sent_at=datetime.now(timezone.utc) if status == DmEventStatus.sent else None,
        )
        self.db.add(event)
        await self.db.commit()
        await self.db.refresh(event)
        return event

    async def mark_replied(self, event_id: UUID) -> DmEvent:
        result = await self.db.execute(select(DmEvent).where(DmEvent.id == event_id))
        event = result.scalar_one()
        event.status     = DmEventStatus.replied
        event.replied_at = datetime.now(timezone.utc)
        await self.db.commit()
        await self.db.refresh(event)
        return event
