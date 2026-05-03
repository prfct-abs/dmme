from datetime import datetime, timedelta, timezone
from typing import Optional

from jose import jwt
from passlib.context import CryptContext
from sqlalchemy.ext.asyncio import AsyncSession

from app.config import settings
from app.models.user import User
from app.repositories.user_repo import UserRepository

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class AuthService:
    def __init__(self, db: AsyncSession):
        self.db   = db
        self.repo = UserRepository(db)

    # ── Password helpers ────────────────────────────────────────────────────
    @staticmethod
    def hash_password(plain: str) -> str:
        return pwd_context.hash(plain)

    @staticmethod
    def verify_password(plain: str, hashed: str) -> bool:
        return pwd_context.verify(plain, hashed)

    # ── JWT helpers ──────────────────────────────────────────────────────────
    @staticmethod
    def create_access_token(user_id: str) -> str:
        expire  = datetime.now(timezone.utc) + timedelta(minutes=settings.JWT_EXPIRE_MINUTES)
        payload = {"sub": user_id, "exp": expire, "type": "access"}
        return jwt.encode(payload, settings.JWT_SECRET, algorithm=settings.JWT_ALGORITHM)

    @staticmethod
    def create_refresh_token(user_id: str) -> str:
        expire  = datetime.now(timezone.utc) + timedelta(days=30)
        payload = {"sub": user_id, "exp": expire, "type": "refresh"}
        return jwt.encode(payload, settings.JWT_SECRET, algorithm=settings.JWT_ALGORITHM)

    @staticmethod
    def decode_token(token: str) -> Optional[dict]:
        try:
            return jwt.decode(token, settings.JWT_SECRET, algorithms=[settings.JWT_ALGORITHM])
        except Exception:
            return None

    # ── Authenticate ─────────────────────────────────────────────────────────
    async def authenticate(self, email: str, password: str) -> Optional[dict]:
        user = await self.repo.get_by_email(email)
        if not user or not self.verify_password(password, user.password_hash):
            return None
        return self._build_token_response(user)

    # ── Refresh token ────────────────────────────────────────────────────────
    async def refresh(self, refresh_token: str) -> Optional[dict]:
        payload = self.decode_token(refresh_token)
        if not payload or payload.get("type") != "refresh":
            return None
        user = await self.repo.get_by_id(payload["sub"])
        if not user:
            return None
        return self._build_token_response(user)

    # ── OAuth ────────────────────────────────────────────────────────────────
    @staticmethod
    def get_oauth_url(platform: str) -> str:
        urls = {
            "instagram": (
                f"https://api.instagram.com/oauth/authorize"
                f"?client_id={settings.INSTAGRAM_APP_ID}"
                f"&redirect_uri={settings.INSTAGRAM_REDIRECT_URI}"
                f"&scope=instagram_basic,instagram_manage_messages"
                f"&response_type=code"
            ),
            "twitter": (
                f"https://twitter.com/i/oauth2/authorize"
                f"?response_type=code&client_id={settings.TWITTER_CLIENT_ID}"
                f"&scope=dm.read+dm.write+tweet.read+users.read"
            ),
        }
        return urls.get(platform, "/")

    async def handle_oauth_callback(self, platform: str, code: str):
        """Exchange code for access token and upsert SocialAccount."""
        import httpx
        from app.repositories.account_repo import AccountRepository

        if platform == "instagram":
            resp = httpx.post("https://api.instagram.com/oauth/access_token", data={
                "client_id":     settings.INSTAGRAM_APP_ID,
                "client_secret": settings.INSTAGRAM_APP_SECRET,
                "grant_type":    "authorization_code",
                "redirect_uri":  settings.INSTAGRAM_REDIRECT_URI,
                "code":          code,
            })
            data = resp.json()
            platform_user_id = str(data["user_id"])
            access_token     = data["access_token"]
        else:
            raise ValueError(f"OAuth not implemented for {platform}")

        # TODO: fetch platform username and upsert social account
        account_repo = AccountRepository(self.db)
        return await account_repo.upsert(platform, platform_user_id, access_token)

    # ── Internal ─────────────────────────────────────────────────────────────
    def _build_token_response(self, user: User) -> dict:
        return {
            "access_token":  self.create_access_token(str(user.id)),
            "refresh_token": self.create_refresh_token(str(user.id)),
            "expires_in":    settings.JWT_EXPIRE_MINUTES * 60,
            "token_type":    "bearer",
            "user":          user,
        }
