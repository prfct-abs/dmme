from sqlalchemy import String, Enum as PgEnum
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base, UUIDMixin, TimestampMixin

import enum

class UserPlan(str, enum.Enum):
    free     = "free"
    pro      = "pro"
    business = "business"


class User(Base, UUIDMixin, TimestampMixin):
    __tablename__ = "users"

    email:         Mapped[str] = mapped_column(String(255), unique=True, nullable=False, index=True)
    name:          Mapped[str] = mapped_column(String(255), nullable=False)
    password_hash: Mapped[str] = mapped_column(String(255), nullable=False)
    plan:          Mapped[UserPlan] = mapped_column(PgEnum(UserPlan), default=UserPlan.free)

    social_accounts = relationship("SocialAccount", back_populates="user", cascade="all, delete-orphan")
    campaigns       = relationship("Campaign",      back_populates="user", cascade="all, delete-orphan")
