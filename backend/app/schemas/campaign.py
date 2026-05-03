from uuid import UUID
from pydantic import BaseModel, Field


class TriggerConfigSchema(BaseModel):
    type: str                          # comment_keyword | story_reply | new_follower | dm_keyword
    keywords: list[str] | None = None
    reply_to: str | None = None


class MessageTemplateSchema(BaseModel):
    body: str
    media_url: str | None = None
    cta_url:   str | None = None


class CampaignCreate(BaseModel):
    name:               str
    platform:           str
    social_account_id:  UUID
    trigger_config:     TriggerConfigSchema
    message_template:   MessageTemplateSchema
    daily_limit:        int = Field(default=50, ge=1, le=500)


class CampaignUpdate(BaseModel):
    name:             str | None = None
    trigger_config:   TriggerConfigSchema | None = None
    message_template: MessageTemplateSchema | None = None
    daily_limit:      int | None = None


class CampaignResponse(BaseModel):
    id:                UUID
    name:              str
    platform:          str
    status:            str
    social_account_id: UUID
    trigger_config:    dict
    message_template:  dict
    daily_limit:       int
    created_at:        str
    updated_at:        str

    model_config = {"from_attributes": True}
