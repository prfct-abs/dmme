import hashlib
import hmac

from fastapi import APIRouter, Depends, Header, HTTPException, Request
from sqlalchemy.ext.asyncio import AsyncSession

from app.config import settings
from app.dependencies import get_db
from app.services.webhook_service import WebhookService

router = APIRouter()


def _verify_instagram_signature(body: bytes, x_hub_signature: str | None) -> bool:
    if not x_hub_signature:
        return False
    expected = "sha256=" + hmac.new(
        settings.INSTAGRAM_APP_SECRET.encode(), body, hashlib.sha256
    ).hexdigest()
    return hmac.compare_digest(expected, x_hub_signature)


@router.get("/instagram")
async def instagram_verify(hub_mode: str, hub_verify_token: str, hub_challenge: str):
    """Instagram webhook verification handshake."""
    if hub_mode == "subscribe" and hub_verify_token == settings.JWT_SECRET:
        return int(hub_challenge)
    raise HTTPException(status_code=403, detail="Verification failed")


@router.post("/instagram")
async def instagram_events(
    request: Request,
    x_hub_signature_256: str | None = Header(None),
    db: AsyncSession = Depends(get_db),
):
    body = await request.body()
    if not _verify_instagram_signature(body, x_hub_signature_256):
        raise HTTPException(status_code=403, detail="Invalid signature")

    payload = await request.json()
    svc = WebhookService(db)
    await svc.handle_instagram(payload)
    return {"status": "ok"}


@router.post("/twitter")
async def twitter_events(request: Request, db: AsyncSession = Depends(get_db)):
    payload = await request.json()
    svc = WebhookService(db)
    await svc.handle_twitter(payload)
    return {"status": "ok"}
