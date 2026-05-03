from contextlib import asynccontextmanager

from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware

from app.config import settings
from app.routers import auth, campaigns, webhooks, analytics, accounts
from app.workers.celery_app import celery_app  # noqa: F401 – ensures tasks are registered


# ── WebSocket connection manager ────────────────────────────────────────────
class ConnectionManager:
    def __init__(self):
        self.active: list[WebSocket] = []

    async def connect(self, ws: WebSocket):
        await ws.accept()
        self.active.append(ws)

    def disconnect(self, ws: WebSocket):
        self.active.remove(ws)

    async def broadcast(self, message: dict):
        for ws in self.active:
            await ws.send_json(message)


manager = ConnectionManager()


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: add DB init, Redis ping, etc. here
    print("🚀 AutoDM API starting up…")
    yield
    print("🛑 AutoDM API shutting down…")


# ── App factory ─────────────────────────────────────────────────────────────
app = FastAPI(
    title="AutoDM API",
    description="Automate your Instagram, X, and LinkedIn DMs",
    version="1.0.0",
    lifespan=lifespan,
    docs_url="/docs",
    redoc_url="/redoc",
)

# ── CORS ────────────────────────────────────────────────────────────────────
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ── Routers ─────────────────────────────────────────────────────────────────
app.include_router(auth.router,      prefix="/api/v1/auth",      tags=["Auth"])
app.include_router(campaigns.router, prefix="/api/v1/campaigns",  tags=["Campaigns"])
app.include_router(webhooks.router,  prefix="/api/v1/webhooks",   tags=["Webhooks"])
app.include_router(analytics.router, prefix="/api/v1/analytics",  tags=["Analytics"])
app.include_router(accounts.router,  prefix="/api/v1/accounts",   tags=["Accounts"])


# ── WebSocket endpoint ──────────────────────────────────────────────────────
@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket, token: str | None = None):
    # TODO: Validate JWT token before accepting
    await manager.connect(websocket)
    try:
        while True:
            await websocket.receive_text()   # Keep alive / accept pings
    except WebSocketDisconnect:
        manager.disconnect(websocket)


# ── Health check ────────────────────────────────────────────────────────────
@app.get("/health", tags=["Health"])
async def health():
    return {"status": "ok", "version": "1.0.0"}
