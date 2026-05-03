from uuid import UUID

from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.dependencies import get_db, get_current_user

router = APIRouter()


@router.get("/")
async def list_accounts(db: AsyncSession = Depends(get_db), current_user=Depends(get_current_user)):
    from app.repositories.account_repo import AccountRepository
    repo = AccountRepository(db)
    return await repo.get_by_user(current_user.id)


@router.delete("/{account_id}", status_code=status.HTTP_204_NO_CONTENT)
async def disconnect_account(
    account_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_user),
):
    from app.repositories.account_repo import AccountRepository
    repo = AccountRepository(db)
    await repo.delete(account_id, current_user.id)
