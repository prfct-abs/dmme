from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.dependencies import get_db, get_current_user
from app.schemas.auth import LoginRequest, TokenResponse, UserResponse
from app.services.auth_service import AuthService

router = APIRouter()


@router.post("/login", response_model=TokenResponse)
async def login(payload: LoginRequest, db: AsyncSession = Depends(get_db)):
    svc = AuthService(db)
    result = await svc.authenticate(payload.email, payload.password)
    if not result:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    return result


@router.get("/me", response_model=UserResponse)
async def me(current_user=Depends(get_current_user)):
    return current_user


@router.post("/refresh", response_model=TokenResponse)
async def refresh_token(token: str, db: AsyncSession = Depends(get_db)):
    svc = AuthService(db)
    result = await svc.refresh(token)
    if not result:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid refresh token")
    return result


@router.get("/oauth/{platform}")
async def oauth_redirect(platform: str):
    """Redirect user to platform OAuth consent screen."""
    from app.services.auth_service import AuthService
    url = AuthService.get_oauth_url(platform)
    from fastapi.responses import RedirectResponse
    return RedirectResponse(url)


@router.get("/oauth/{platform}/callback")
async def oauth_callback(platform: str, code: str, db: AsyncSession = Depends(get_db)):
    """Handle OAuth callback, exchange code for token, store social account."""
    svc = AuthService(db)
    account = await svc.handle_oauth_callback(platform, code)
    return {"status": "connected", "platform": platform, "username": account.platform_username}
