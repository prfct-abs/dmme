"""Initial schema

Revision ID: 001
Create Date: 2026-03-26
"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import UUID, JSONB

revision = "001"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "users",
        sa.Column("id",            UUID(as_uuid=True), primary_key=True, server_default=sa.text("gen_random_uuid()")),
        sa.Column("email",         sa.String(255), nullable=False, unique=True),
        sa.Column("name",          sa.String(255), nullable=False),
        sa.Column("password_hash", sa.String(255), nullable=False),
        sa.Column("plan",          sa.String(50),  nullable=False, server_default="free"),
        sa.Column("created_at",    sa.DateTime(timezone=True), server_default=sa.text("now()")),
        sa.Column("updated_at",    sa.DateTime(timezone=True), server_default=sa.text("now()")),
    )
    op.create_index("ix_users_email", "users", ["email"], unique=True)

    op.create_table(
        "social_accounts",
        sa.Column("id",                UUID(as_uuid=True), primary_key=True, server_default=sa.text("gen_random_uuid()")),
        sa.Column("user_id",           UUID(as_uuid=True), sa.ForeignKey("users.id", ondelete="CASCADE"), nullable=False),
        sa.Column("platform",          sa.String(50),   nullable=False),
        sa.Column("platform_user_id",  sa.String(255),  nullable=False),
        sa.Column("platform_username", sa.String(255),  nullable=False, server_default=""),
        sa.Column("access_token",      sa.String(2048), nullable=False),
        sa.Column("refresh_token",     sa.String(2048)),
        sa.Column("token_expires_at",  sa.DateTime(timezone=True)),
        sa.Column("is_active",         sa.Boolean, nullable=False, server_default="true"),
        sa.Column("created_at",        sa.DateTime(timezone=True), server_default=sa.text("now()")),
        sa.Column("updated_at",        sa.DateTime(timezone=True), server_default=sa.text("now()")),
    )

    op.create_table(
        "campaigns",
        sa.Column("id",                UUID(as_uuid=True), primary_key=True, server_default=sa.text("gen_random_uuid()")),
        sa.Column("user_id",           UUID(as_uuid=True), sa.ForeignKey("users.id", ondelete="CASCADE"), nullable=False),
        sa.Column("social_account_id", UUID(as_uuid=True), sa.ForeignKey("social_accounts.id", ondelete="CASCADE"), nullable=False),
        sa.Column("name",              sa.String(255), nullable=False),
        sa.Column("platform",          sa.String(50),  nullable=False),
        sa.Column("status",            sa.String(50),  nullable=False, server_default="draft"),
        sa.Column("trigger_config",    JSONB, nullable=False, server_default="{}"),
        sa.Column("message_template",  JSONB, nullable=False, server_default="{}"),
        sa.Column("daily_limit",       sa.Integer, nullable=False, server_default="50"),
        sa.Column("created_at",        sa.DateTime(timezone=True), server_default=sa.text("now()")),
        sa.Column("updated_at",        sa.DateTime(timezone=True), server_default=sa.text("now()")),
    )
    op.create_index("ix_campaigns_user_id",   "campaigns", ["user_id"])
    op.create_index("ix_campaigns_status",    "campaigns", ["status"])

    op.create_table(
        "dm_events",
        sa.Column("id",                    UUID(as_uuid=True), primary_key=True, server_default=sa.text("gen_random_uuid()")),
        sa.Column("campaign_id",           UUID(as_uuid=True), sa.ForeignKey("campaigns.id", ondelete="CASCADE"), nullable=False),
        sa.Column("recipient_platform_id", sa.String(255), nullable=False),
        sa.Column("recipient_username",    sa.String(255)),
        sa.Column("status",                sa.String(50),  nullable=False, server_default="pending"),
        sa.Column("message_snapshot",      JSONB, nullable=False, server_default="{}"),
        sa.Column("sent_at",               sa.DateTime(timezone=True)),
        sa.Column("replied_at",            sa.DateTime(timezone=True)),
        sa.Column("created_at",            sa.DateTime(timezone=True), server_default=sa.text("now()")),
        sa.Column("updated_at",            sa.DateTime(timezone=True), server_default=sa.text("now()")),
    )
    op.create_index("ix_dm_events_campaign_id", "dm_events", ["campaign_id"])
    op.create_index("ix_dm_events_status",      "dm_events", ["status"])


def downgrade() -> None:
    op.drop_table("dm_events")
    op.drop_table("campaigns")
    op.drop_table("social_accounts")
    op.drop_table("users")
