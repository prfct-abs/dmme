import enum
import uuid

from sqlalchemy import Boolean, Enum as PgEnum, ForeignKey, Integer, String
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base, UUIDMixin, TimestampMixin


class CampaignStatus(str, enum.Enum):
    active = "active"
    paused = "paused"
    draft  = "draft"


class TriggerType(str, enum.Enum):
    comment_keyword = "comment_keyword"
    story_reply     = "story_reply"
    new_follower    = "new_follower"
    dm_keyword      = "dm_keyword"


class Campaign(Base, UUIDMixin, TimestampMixin):
    __tablename__ = "campaigns"

    user_id:            Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    social_account_id:  Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("social_accounts.id"), nullable=False)
    name:               Mapped[str]       = mapped_column(String(255), nullable=False)
    platform:           Mapped[str]       = mapped_column(String(50), nullable=False)
    status:             Mapped[CampaignStatus] = mapped_column(PgEnum(CampaignStatus), default=CampaignStatus.draft)
    trigger_config:     Mapped[dict]      = mapped_column(JSONB, nullable=False, default=dict)
    message_template:   Mapped[dict]      = mapped_column(JSONB, nullable=False, default=dict)
    daily_limit:        Mapped[int]       = mapped_column(Integer, default=50)

    user           = relationship("User",          back_populates="campaigns")
    social_account = relationship("SocialAccount", back_populates="campaigns")
    dm_events      = relationship("DmEvent",       back_populates="campaign", cascade="all, delete-orphan")
