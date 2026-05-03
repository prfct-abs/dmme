from uuid import UUID

from sqlalchemy import select, and_
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.social_account import SocialAccount


class AccountRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_by_user(self, user_id: UUID) -> list[SocialAccount]:
        result = await self.db.execute(
            select(SocialAccount).where(SocialAccount.user_id == user_id)
        )
        return list(result.scalars().all())

    async def upsert(self, platform: str, platform_user_id: str, access_token: str,
                     platform_username: str = "", user_id: UUID | None = None) -> SocialAccount:
        result = await self.db.execute(
            select(SocialAccount).where(
                and_(SocialAccount.platform == platform,
                     SocialAccount.platform_user_id == platform_user_id)
            )
        )
        acct = result.scalar_one_or_none()
        if acct:
            acct.access_token = access_token
            acct.is_active    = True
        else:
            acct = SocialAccount(
                platform=platform,
                platform_user_id=platform_user_id,
                platform_username=platform_username,
                access_token=access_token,
                user_id=user_id,
            )
            self.db.add(acct)
        await self.db.commit()
        await self.db.refresh(acct)
        return acct

    async def delete(self, account_id: UUID, user_id: UUID) -> None:
        result = await self.db.execute(
            select(SocialAccount).where(
                and_(SocialAccount.id == account_id, SocialAccount.user_id == user_id)
            )
        )
        acct = result.scalar_one_or_none()
        if acct:
            await self.db.delete(acct)
            await self.db.commit()
