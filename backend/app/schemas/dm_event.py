from uuid import UUID
from pydantic import BaseModel


class DmEventResponse(BaseModel):
    id:                    UUID
    campaign_id:           UUID
    recipient_platform_id: str
    recipient_username:    str | None = None
    status:                str
    message_snapshot:      dict
    sent_at:               str | None = None
    replied_at:            str | None = None

    model_config = {"from_attributes": True}
