import uuid

from sqlalchemy import Boolean, ForeignKey, String, DateTime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base, UUIDMixin, TimestampMixin


class SocialAccount(Base, UUIDMixin, TimestampMixin):
    __tablename__ = "social_accounts"

    user_id:            Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    platform:           Mapped[str]       = mapped_column(String(50),  nullable=False)
    platform_user_id:   Mapped[str]       = mapped_column(String(255), nullable=False)
    platform_username:  Mapped[str]       = mapped_column(String(255), nullable=False)
    access_token:       Mapped[str]       = mapped_column(String(2048), nullable=False)
    refresh_token:      Mapped[str | None] = mapped_column(String(2048))
    token_expires_at:   Mapped[str | None] = mapped_column(DateTime(timezone=True))
    is_active:          Mapped[bool]      = mapped_column(Boolean, default=True)

    user      = relationship("User",     back_populates="social_accounts")
    campaigns = relationship("Campaign", back_populates="social_account")
