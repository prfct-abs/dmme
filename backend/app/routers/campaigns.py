from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.dependencies import get_db, get_current_user
from app.schemas.campaign import CampaignCreate, CampaignResponse, CampaignUpdate
from app.services.campaign_service import CampaignService

router = APIRouter()


@router.get("/", response_model=list[CampaignResponse])
async def list_campaigns(
    page: int = 1,
    page_size: int = 20,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_user),
):
    svc = CampaignService(db)
    return await svc.list_for_user(current_user.id, page=page, page_size=page_size)


@router.post("/", response_model=CampaignResponse, status_code=status.HTTP_201_CREATED)
async def create_campaign(
    payload: CampaignCreate,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_user),
):
    svc = CampaignService(db)
    return await svc.create(current_user.id, payload)


@router.get("/{campaign_id}", response_model=CampaignResponse)
async def get_campaign(campaign_id: UUID, db: AsyncSession = Depends(get_db), current_user=Depends(get_current_user)):
    svc = CampaignService(db)
    camp = await svc.get(campaign_id, current_user.id)
    if not camp:
        raise HTTPException(status_code=404, detail="Campaign not found")
    return camp


@router.put("/{campaign_id}", response_model=CampaignResponse)
async def update_campaign(
    campaign_id: UUID,
    payload: CampaignUpdate,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_user),
):
    svc = CampaignService(db)
    return await svc.update(campaign_id, current_user.id, payload)


@router.patch("/{campaign_id}/toggle", response_model=CampaignResponse)
async def toggle_campaign(campaign_id: UUID, db: AsyncSession = Depends(get_db), current_user=Depends(get_current_user)):
    svc = CampaignService(db)
    return await svc.toggle(campaign_id, current_user.id)


@router.delete("/{campaign_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_campaign(campaign_id: UUID, db: AsyncSession = Depends(get_db), current_user=Depends(get_current_user)):
    svc = CampaignService(db)
    await svc.delete(campaign_id, current_user.id)
