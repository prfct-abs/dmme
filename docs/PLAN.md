# 🤖 AutoDM — Scaffolding Plan

> **Stack:** Nuxt 3 + Pinia (frontend) · FastAPI + Celery + PostgreSQL (backend)  
> Check off each item as it is created. Delete this file when the project is fully scaffolded.

---

## 🖥️ Frontend — Nuxt 3

### Foundation
- [x] `frontend/nuxt.config.ts` — Nuxt config (modules, runtimeConfig, Nitro proxy)
- [x] `frontend/app.vue` — Root shell, global CSS tokens, transitions
- [x] `frontend/package.json` — Dependencies
- [x] `frontend/.env.example` — Environment variable template
- [x] `frontend/tailwind.config.ts` — Tailwind theme config
- [x] `frontend/types/index.ts` — Shared TypeScript interfaces (Campaign, User, DmEvent, etc.)

### Layouts
- [x] `frontend/layouts/default.vue` — Dashboard shell (sidebar + topbar + main slot)
- [x] `frontend/layouts/auth.vue` — Centered auth card shell

### Pages
- [ ] `frontend/pages/login.vue` — Login / OAuth entry point
- [ ] `frontend/pages/dashboard/index.vue` — Overview metrics + recent activity
- [ ] `frontend/pages/campaigns/index.vue` — Campaign list + create button
- [ ] `frontend/pages/campaigns/[id].vue` — Campaign detail (trigger builder + message editor)
- [ ] `frontend/pages/analytics/index.vue` — Charts, DM event feed
- [ ] `frontend/pages/accounts/index.vue` — Connected social accounts
- [ ] `frontend/pages/templates/index.vue` — Message template library

### Components
- [x] `frontend/components/App/AppSidebar.vue` — Navigation sidebar
- [x] `frontend/components/App/AppTopBar.vue` — Top bar (user menu, search)
- [x] `frontend/components/App/AppToast.vue` — Global toast notifications
- [ ] `frontend/components/Campaign/CampaignCard.vue` — Campaign list card
- [ ] `frontend/components/Campaign/TriggerBuilder.vue` — Visual trigger configurator
- [ ] `frontend/components/Campaign/MessageEditor.vue` — Template editor with variables
- [ ] `frontend/components/Analytics/MetricsChart.vue` — Chart.js wrapper

### Pinia Stores
- [x] `frontend/stores/auth.store.ts` — Auth state (user, token, login/logout)
- [x] `frontend/stores/campaign.store.ts` — Campaigns CRUD + filters
- [x] `frontend/stores/analytics.store.ts` — Metrics + DM event log
- [x] `frontend/stores/account.store.ts` — Connected social accounts
- [x] `frontend/stores/notif.store.ts` — Toast / notification queue

### Composables
- [x] `frontend/composables/useApi.ts` — useFetch wrapper with JWT headers
- [x] `frontend/composables/useWebSocket.ts` — WebSocket connection to FastAPI
- [x] `frontend/composables/useErrorHandler.ts` — Global error to toast mapper

### Nitro Server (BFF Layer)
- [x] `frontend/server/api/campaigns.get.ts` — Proxy GET /campaigns to FastAPI
- [x] `frontend/server/api/campaigns.post.ts` — Proxy POST /campaigns to FastAPI
- [x] `frontend/server/api/auth/login.post.ts` — OAuth token exchange
- [x] `frontend/server/middleware/auth.ts` — JWT guard for server routes

---

## ⚙️ Backend — FastAPI (Python)

### Foundation
- [x] `backend/app/main.py` — FastAPI app, CORS, router registration, WebSocket endpoint
- [x] `backend/app/config.py` — pydantic-settings env var model
- [x] `backend/app/dependencies.py` — DI: async DB session, get_current_user
- [x] `backend/requirements.txt` — All Python dependencies
- [ ] `backend/.env.example` — Environment variable template

### Routers
- [x] `backend/app/routers/auth.py` — OAuth2 login, token refresh, social connect
- [x] `backend/app/routers/campaigns.py` — CRUD, toggle active, clone
- [x] `backend/app/routers/webhooks.py` — Instagram / X / LinkedIn webhook receivers
- [x] `backend/app/routers/analytics.py` — Metrics aggregation endpoints
- [x] `backend/app/routers/accounts.py` — Connected social account management

### Services (Business Logic)
- [ ] `backend/app/services/auth_service.py` — JWT creation/verification, OAuth flows
- [ ] `backend/app/services/campaign_service.py` — Trigger evaluation engine
- [ ] `backend/app/services/dm_service.py` — Message formatting + platform dispatch
- [ ] `backend/app/services/webhook_service.py` — HMAC verification + event parsing
- [ ] `backend/app/services/analytics_service.py` — Event aggregation queries
- [ ] `backend/app/services/ai_service.py` — (Optional) LLM message personalization

### SQLAlchemy Models
- [x] `backend/app/models/base.py` — Declarative base + UUID mixin
- [x] `backend/app/models/user.py` — User model
- [x] `backend/app/models/social_account.py` — Connected social account model
- [x] `backend/app/models/campaign.py` — Campaign + Trigger models
- [x] `backend/app/models/dm_event.py` — DM event log model

### Pydantic Schemas
- [x] `backend/app/schemas/auth.py` — Login, token, user response schemas
- [x] `backend/app/schemas/campaign.py` — Campaign create/update/response schemas
- [ ] `backend/app/schemas/dm_event.py` — DM event schemas

### Celery Workers
- [x] `backend/app/workers/celery_app.py` — Celery app + Redis broker config
- [x] `backend/app/workers/dm_tasks.py` — send_dm task with retry logic
- [ ] `backend/app/workers/beat_schedule.py` — Celery Beat periodic task schedule

### Database Migrations
- [ ] `backend/alembic/env.py` — Alembic config (async engine)
- [ ] `backend/alembic/versions/001_initial_schema.py` — Initial migration

---

## 🐳 Infrastructure

- [x] `docker-compose.yml` — Nuxt + FastAPI + PostgreSQL + Redis + Celery worker
- [x] `frontend/Dockerfile` — Nuxt 3 production image
- [x] `backend/Dockerfile` — FastAPI production image (uvicorn)
- [ ] `.env.example` — Root-level combined env template
- [x] `.gitignore` — Ignore .env, __pycache__, .nuxt, node_modules, etc.

---

## 📊 Progress

| Area | Done | Total |
|---|---|---|
| Frontend Foundation | 6 | 6 |
| Layouts | 2 | 2 |
| Pages | 0 | 7 |
| Components | 3 | 7 |
| Pinia Stores | 5 | 5 |
| Composables | 3 | 3 |
| Nitro Server | 4 | 4 |
| Backend Foundation | 4 | 5 |
| Routers | 5 | 5 |
| Services | 0 | 6 |
| Models | 5 | 5 |
| Schemas | 2 | 3 |
| Workers | 2 | 3 |
| Migrations | 0 | 2 |
| Infrastructure | 4 | 5 |
| **TOTAL** | **45** | **73** |
