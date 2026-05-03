import enum
import uuid

from sqlalchemy import DateTime, Enum as PgEnum, ForeignKey, String
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base, UUIDMixin, TimestampMixin


class DmEventStatus(str, enum.Enum):
    pending = "pending"
    sent    = "sent"
    failed  = "failed"
    replied = "replied"


class DmEvent(Base, UUIDMixin, TimestampMixin):
    __tablename__ = "dm_events"

    campaign_id:           Mapped[uuid.UUID]     = mapped_column(UUID(as_uuid=True), ForeignKey("campaigns.id"), nullable=False)
    recipient_platform_id: Mapped[str]           = mapped_column(String(255), nullable=False)
    recipient_username:    Mapped[str | None]     = mapped_column(String(255))
    status:                Mapped[DmEventStatus] = mapped_column(PgEnum(DmEventStatus), default=DmEventStatus.pending)
    message_snapshot:      Mapped[dict]          = mapped_column(JSONB, nullable=False, default=dict)
    sent_at:               Mapped[str | None]    = mapped_column(DateTime(timezone=True))
    replied_at:            Mapped[str | None]    = mapped_column(DateTime(timezone=True))

    campaign = relationship("Campaign", back_populates="dm_events")
