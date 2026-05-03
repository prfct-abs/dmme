from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.dependencies import get_db, get_current_user
from app.services.analytics_service import AnalyticsService

router = APIRouter()


@router.get("/metrics")
async def get_metrics(
    campaign_id: str | None = None,
    from_date: str | None = None,
    to_date: str | None = None,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_user),
):
    svc = AnalyticsService(db)
    return await svc.get_metrics(
        user_id=current_user.id,
        campaign_id=campaign_id,
        from_date=from_date,
        to_date=to_date,
    )


@router.get("/events")
async def get_events(
    campaign_id: str | None = None,
    limit: int = 50,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_user),
):
    svc = AnalyticsService(db)
    return await svc.get_events(user_id=current_user.id, campaign_id=campaign_id, limit=limit)
