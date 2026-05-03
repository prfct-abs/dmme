# 🤖 Auto DM Platform — Architecture & Design

> A full-stack system for automating social media direct messages, built with **Nuxt 3**, **Pinia**, and a **FastAPI (Python)** backend.

---

## 📐 System Overview

```mermaid
graph TB
    subgraph "Client Layer (Nuxt 3 + Pinia)"
        UI["🖥️ Nuxt 3\n(SSR / SPA / SSG modes)"]
        PINIA["🍍 Pinia Store\n(@pinia/nuxt module)"]
        ROUTER["File-based Routing\n(pages/ → auto Vue Router)"]
        NITRO["⚡ Nitro Server\n(server/api/ proxy routes)"]
        UI <--> PINIA
        UI <--> ROUTER
        UI <--> NITRO
    end

    subgraph "API Gateway"
        GW["🔀 API Gateway / Reverse Proxy\n(Nginx / Caddy)"]
        AUTH["🔐 Auth Middleware\n(JWT Verification)"]
        GW --> AUTH
    end

    subgraph "Backend Services (Python / FastAPI)"
        AS["🔑 Auth Service\n(OAuth 2.0, JWT)"]
        DMS["📨 DM Automation Service\n(Trigger Engine)"]
        CAMS["📋 Campaign Service\n(CRUD, Scheduling)"]
        WBHS["🪝 Webhook Handler\n(Instagram / X / LinkedIn)"]
        QS["📊 Analytics Service\n(Events, Metrics)"]
    end

    subgraph "Background Workers (Celery + Redis)"
        WQ["🔄 Worker Queue\nCelery DM Dispatch Workers"]
        SCHED["⏰ Celery Beat\nScheduled Campaigns"]
    end

    subgraph "External Platform APIs"
        IG["📸 Instagram\nMessenger API"]
        TW["🐦 X (Twitter)\nAPI v2"]
        LI["💼 LinkedIn\nMessaging API"]
    end

    subgraph "Data Layer"
        PG[("🐘 PostgreSQL\n(Primary Store)")]
        REDIS[("⚡ Redis\n(Cache + Queue)")]
        S3["☁️ S3 / Supabase Storage\n(Media Assets)"]
    end

    NITRO -->|"Server-side API calls"| GW
    UI -->|"HTTPS REST / WebSocket"| GW
    AUTH --> AS
    AUTH --> DMS
    AUTH --> CAMS
    AUTH --> WBHS
    AUTH --> QS

    DMS --> WQ
    CAMS --> SCHED
    SCHED --> WQ

    WQ -->|"Rate-limited dispatch"| IG
    WQ -->|"Rate-limited dispatch"| TW
    WQ -->|"Rate-limited dispatch"| LI

    IG -->|"Incoming webhooks"| WBHS
    TW -->|"Incoming webhooks"| WBHS
    LI -->|"Incoming webhooks"| WBHS

    AS --> PG
    DMS --> PG
    CAMS --> PG
    QS --> PG
    WBHS --> DMS

    AS --> REDIS
    DMS --> REDIS
    CAMS --> S3
```

---

## 🎨 Frontend Architecture (Nuxt 3 + Pinia)

```mermaid
graph TD
    subgraph "Nuxt 3 Application"
        APP["app.vue\n(Root shell + NuxtLayout)"]

        subgraph "Layouts (layouts/)"
            LAY_D["default.vue\n(Sidebar + TopBar)"]
            LAY_A["auth.vue\n(Centered auth shell)"]
        end

        subgraph "Pages (pages/) — File-based Routing"
            LP["pages/login.vue"]
            DASH["pages/dashboard/index.vue"]
            CAMP["pages/campaigns/index.vue"]
            CAMP_D["pages/campaigns/[id].vue"]
            ANA["pages/analytics/index.vue"]
            CONN["pages/accounts/index.vue"]
            TEMP["pages/templates/index.vue"]
        end

        subgraph "Components (components/)"
            NAV["AppSidebar.vue"]
            TB["AppTopBar.vue"]
            CCARD["CampaignCard.vue"]
            TRIG["TriggerBuilder.vue"]
            MBED["MessageEditor.vue"]
            CHART["MetricsChart.vue"]
            TOASTS["AppToast.vue"]
        end

        subgraph "🍍 Pinia Stores (stores/)"
            US["useAuthStore\n(user, token, session)"]
            CS["useCampaignStore\n(campaigns[], active, filters)"]
            ACCS["useAccountStore\n(connected socials)"]
            AS2["useAnalyticsStore\n(metrics, events)"]
            NS["useNotifStore\n(toasts, alerts)"]
        end

        subgraph "Composables (composables/) — Auto-imported"
            UAP["useApi()\n(useFetch wrapper + JWT headers)"]
            UWS["useWebSocket()\n(real-time campaign events)"]
            UERR["useErrorHandler()"]
            UAD["useAsyncData()\n(SSR-safe data fetching)"]
        end

        subgraph "Nuxt Server (server/api/) — Nitro"
            SA1["server/api/campaigns.get.ts"]
            SA2["server/api/auth/[...].ts"]
            SA3["server/middleware/auth.ts"]
        end
    end

    APP --> LAY_D
    APP --> LAY_A
    LAY_D --> NAV
    LAY_D --> TB
    LAY_D --> TOASTS
    LAY_A --> LP

    LAY_D --> DASH
    LAY_D --> CAMP
    LAY_D --> ANA
    LAY_D --> CONN
    LAY_D --> TEMP

    CAMP --> CCARD
    CAMP --> CAMP_D
    CAMP_D --> TRIG
    CAMP_D --> MBED
    ANA --> CHART

    DASH --> CS
    CAMP --> CS
    ANA --> AS2
    CONN --> ACCS
    NAV --> US

    CS --> UAP
    AS2 --> UAP
    ACCS --> UAP
    US --> UAP
    DASH --> UWS
    DASH --> UAD

    UAP --> SA1
    SA1 -->|"Proxies to FastAPI"| SA2
```

> [!NOTE]
> Nuxt 3's **`server/api/`** routes (powered by **Nitro**) act as a lightweight BFF (Backend-for-Frontend) proxy layer. They handle cookie-based auth, token injection, and CORS — so the browser never directly calls the FastAPI backend.

---

## 🗂️ Pinia Store Design

```mermaid
classDiagram
    class useAuthStore {
        +user: User | null
        +token: string | null
        +isAuthenticated: boolean
        +login(credentials)
        +logout()
        +refreshToken()
        +connectSocialAccount(platform)
    }

    class useCampaignStore {
        +campaigns: Campaign[]
        +activeCampaign: Campaign | null
        +isLoading: boolean
        +filters: FilterState
        +fetchCampaigns()
        +createCampaign(data)
        +updateCampaign(id, data)
        +deleteCampaign(id)
        +toggleCampaign(id)
    }

    class useAnalyticsStore {
        +metrics: PlatformMetrics
        +events: DmEvent[]
        +dateRange: DateRange
        +fetchMetrics(range)
        +fetchEvents(campaignId)
    }

    class useAccountStore {
        +accounts: SocialAccount[]
        +fetchAccounts()
        +disconnectAccount(id)
        +refreshTokenForAccount(id)
    }

    class useNotifStore {
        +toasts: Toast[]
        +addToast(msg, type)
        +removeToast(id)
    }

    useAuthStore --> useCampaignStore : "guards campaign actions"
    useAuthStore --> useAccountStore : "links connected accounts"
    useCampaignStore --> useAnalyticsStore : "campaign ID reference"
```

---

## 🔧 Backend Service Architecture (Python / FastAPI)

```mermaid
graph LR
    subgraph "FastAPI Application"
        direction TB
        PLUG["Middleware\n(CORS, JWT Auth, Rate Limit, OpenAPI/Swagger)"]

        subgraph "Routers (APIRouter)"
            R_AUTH["/auth/*\nOAuth2, Login, Refresh Token"]
            R_CAMP["/campaigns/*\nCRUD, Toggle, Clone"]
            R_TEMP["/templates/*\nMessage Templates"]
            R_ANA["/analytics/*\nEvents, Funnels"]
            R_WH["/webhooks/*\nIG, X, LinkedIn"]
            R_ACC["/accounts/*\nConnected Socials"]
        end

        subgraph "Service Layer"
            SVC_AUTH["AuthService\nJWT + OAuth2 (python-jose)"]
            SVC_CAMP["CampaignService\nTrigger evaluation"]
            SVC_DM["DmService\nMessage formatting + dispatch"]
            SVC_WH["WebhookService\nHMAC validation + event parsing"]
            SVC_ANA["AnalyticsService\nEvent logging + aggregation"]
            SVC_AI["AIService\n(Optional) LLM message personalization"]
        end

        subgraph "Data Access Layer (SQLAlchemy + Alembic)"
            REPO_CAMP["CampaignRepository"]
            REPO_USER["UserRepository"]
            REPO_EVENTS["EventRepository"]
        end

        subgraph "Background Tasks (Celery + Redis)"
            WORKER["DM Dispatch Workers\n(celery workers)"]
            BEAT["Celery Beat\n(Scheduled campaigns)"]
        end
    end

    R_AUTH --> SVC_AUTH
    R_CAMP --> SVC_CAMP
    R_WH --> SVC_WH
    R_ANA --> SVC_ANA
    R_ACC --> SVC_AUTH

    SVC_CAMP --> SVC_DM
    SVC_CAMP --> SVC_AI
    SVC_WH --> SVC_CAMP
    SVC_DM --> WORKER
    BEAT --> WORKER

    SVC_CAMP --> REPO_CAMP
    SVC_AUTH --> REPO_USER
    SVC_ANA --> REPO_EVENTS
```

> [!NOTE]
> FastAPI auto-generates an **interactive Swagger UI** at `/docs` and a **ReDoc** page at `/redoc` — zero extra configuration needed. This makes API development and testing significantly faster.

---

## 🗄️ Database Schema (PostgreSQL)

```mermaid
erDiagram
    USERS {
        uuid id PK
        string email UK
        string name
        string password_hash
        string plan "free | pro | business"
        timestamp created_at
    }

    SOCIAL_ACCOUNTS {
        uuid id PK
        uuid user_id FK
        string platform "instagram | twitter | linkedin"
        string platform_user_id
        string access_token
        string refresh_token
        timestamp token_expires_at
        boolean is_active
    }

    CAMPAIGNS {
        uuid id PK
        uuid user_id FK
        uuid social_account_id FK
        string name
        string status "active | paused | draft"
        string platform
        jsonb trigger_config
        jsonb message_template
        integer daily_limit
        timestamp created_at
    }

    TRIGGERS {
        uuid id PK
        uuid campaign_id FK
        string type "comment_keyword | story_reply | new_follower | webhook"
        jsonb config
    }

    DM_EVENTS {
        uuid id PK
        uuid campaign_id FK
        string recipient_platform_id
        string status "pending | sent | failed | replied"
        jsonb message_snapshot
        timestamp sent_at
        timestamp replied_at
    }

    USERS ||--o{ SOCIAL_ACCOUNTS : "connects"
    USERS ||--o{ CAMPAIGNS : "owns"
    SOCIAL_ACCOUNTS ||--o{ CAMPAIGNS : "used by"
    CAMPAIGNS ||--o{ TRIGGERS : "has"
    CAMPAIGNS ||--o{ DM_EVENTS : "generates"
```

---

## 🔄 Auto DM Trigger Flow

```mermaid
sequenceDiagram
    participant Platform as 📱 Instagram / X
    participant WH as Webhook Handler
    participant TrigEng as Trigger Engine
    participant Queue as Celery Queue
    participant Worker as Celery Worker
    participant DB as PostgreSQL
    participant Redis as Redis Cache

    Platform->>WH: POST /webhooks/instagram (user commented "GUIDE")
    WH->>WH: Validate HMAC signature
    WH->>TrigEng: Fire event {type: "comment", keyword: "GUIDE", user_id: "xyz"}
    TrigEng->>DB: Find matching active campaigns for this trigger
    DB-->>TrigEng: [Campaign A, Campaign B]
    TrigEng->>Redis: Check rate limit (has user xyz been DM'd today?)
    Redis-->>TrigEng: Not rate limited
    TrigEng->>Queue: celery.apply_async(send_dm, {campaignId, recipientId, message})
    Queue->>Worker: Pick up task
    Worker->>Platform: POST /messages (send DM)
    Platform-->>Worker: 200 OK {message_id: "abc"}
    Worker->>DB: Log DM event (status: sent)
    Worker->>Redis: Increment rate limit counter for user xyz
```

---

## 🥞 Recommended Tech Stack

| Layer | Technology | Why |
|---|---|---|
| **Frontend Framework** | **Nuxt 3** (Vue 3 + Nitro + Vite) | SSR/SSG/SPA in one, file-based routing, auto-imports |
| **State Management** | **Pinia** (`@pinia/nuxt` module) | Lightweight, type-safe, SSR-compatible |
| **Routing** | **File-based** (`pages/`) | Zero-config, dynamic routes `[id].vue`, layout system |
| **Data Fetching** | `useFetch` / `useAsyncData` | SSR-aware, deduped, server + client |
| **BFF Proxy Layer** | Nuxt `server/api/` (Nitro) | Hides FastAPI from browser, handles cookies/tokens |
| **UI Component Library** | **Nuxt UI** or **shadcn-vue** | Nuxt-native, accessible, dark mode ready |
| **Charts** | Chart.js + vue-chartjs | Analytics dashboards |
| **Key Nuxt Modules** | `@nuxtjs/tailwindcss`, `@nuxtjs/color-mode`, `nuxt-icon`, `@vueuse/nuxt` | Productivity + UX |
| **Build / SSR Runtime** | Vite (dev) + Nitro (prod server) | Blazing fast dev, edge-deployable prod |
| **Backend Framework** | **FastAPI (Python 3.12+)** | Async-native, auto Swagger docs, Pydantic validation |
| **Auth** | `python-jose` (JWT) + `authlib` (OAuth2) | Social OAuth flows + stateless JWT sessions |
| **Task Queue / Workers** | **Celery + Redis** | Distributed workers, rate limiting, scheduled campaigns |
| **ORM** | **SQLAlchemy 2.0** (async) + **Alembic** | Type-safe queries, auto DB migrations |
| **Data Validation** | **Pydantic v2** | Request/response models, auto docs |
| **Database** | **PostgreSQL** | Relational, robust, JSONB columns for trigger configs |
| **Cache / Rate Limiter** | Redis (`redis-py` async) | Fast lookups, counter-based rate limits |
| **AI Personalization** | OpenAI API / Ollama | Smart message generation (Python excels here) |
| **File Storage** | Supabase Storage or AWS S3 (`boto3`) | Media & template assets |
| **Real-time** | FastAPI WebSockets | Live campaign status updates to Vue frontend |
| **Infrastructure** | Docker + Railway / Render / Fly.io | Easy deployment, auto-scaling |
| **Monitoring** | Sentry SDK + `structlog` | Error tracking, structured JSON logs |

---

## 🏗️ Recommended Folder Structure

```
autodm-app/
├── frontend/                      # Nuxt 3 App
│   ├── app.vue                    # Root shell
│   ├── nuxt.config.ts             # Nuxt config (modules, runtimeConfig)
│   ├── assets/                    # Global CSS, fonts
│   ├── components/                # Auto-imported components
│   │   ├── App/
│   │   │   ├── AppSidebar.vue
│   │   │   └── AppTopBar.vue
│   │   └── Campaign/
│   │       ├── CampaignCard.vue
│   │       └── TriggerBuilder.vue
│   ├── composables/               # Auto-imported composables
│   │   ├── useApi.ts
│   │   ├── useWebSocket.ts
│   │   └── useErrorHandler.ts
│   ├── layouts/                   # Nuxt layouts
│   │   ├── default.vue
│   │   └── auth.vue
│   ├── pages/                     # File-based routes
│   │   ├── login.vue
│   │   ├── dashboard/
│   │   │   └── index.vue
│   │   ├── campaigns/
│   │   │   ├── index.vue
│   │   │   └── [id].vue
│   │   ├── analytics/index.vue
│   │   ├── accounts/index.vue
│   │   └── templates/index.vue
│   ├── server/                    # Nitro server (BFF layer)
│   │   ├── api/
│   │   │   ├── campaigns.get.ts
│   │   │   └── auth/[...].ts
│   │   └── middleware/
│   │       └── auth.ts
│   ├── stores/                    # Pinia stores
│   │   ├── auth.store.ts
│   │   ├── campaign.store.ts
│   │   ├── analytics.store.ts
│   │   └── account.store.ts
│   └── types/                     # TypeScript interfaces
│
└── backend/                       # Python FastAPI
    ├── app/
    │   ├── main.py                # FastAPI app entry point
    │   ├── config.py              # Settings (pydantic-settings)
    │   ├── dependencies.py        # DI: db sessions, current user
    │   ├── routers/               # APIRouter modules
    │   │   ├── auth.py
    │   │   ├── campaigns.py
    │   │   ├── webhooks.py
    │   │   ├── analytics.py
    │   │   └── accounts.py
    │   ├── services/              # Business logic
    │   │   ├── auth_service.py
    │   │   ├── campaign_service.py
    │   │   ├── dm_service.py
    │   │   ├── webhook_service.py
    │   │   └── ai_service.py
    │   ├── models/                # SQLAlchemy ORM models
    │   │   ├── user.py
    │   │   ├── campaign.py
    │   │   └── dm_event.py
    │   ├── schemas/               # Pydantic request/response models
    │   │   ├── campaign.py
    │   │   └── auth.py
    │   ├── repositories/          # DB query logic
    │   ├── workers/               # Celery task definitions
    │   │   ├── celery_app.py
    │   │   └── dm_tasks.py
    │   └── utils/
    ├── alembic/                   # DB migrations
    │   └── versions/
    ├── requirements.txt
    ├── .env
    └── Dockerfile
```

---

> [!TIP]
> **Start with Supabase** for PostgreSQL + Storage, and point your FastAPI backend's SQLAlchemy connection string at Supabase's Postgres instance. You get managed DB, backups, and a dashboard for free — while keeping full control of your API logic.

> [!IMPORTANT]
> Always validate **incoming webhook HMAC signatures** from platforms (Instagram, X) using Python's `hmac` module before processing events. Never trust raw webhook payloads without cryptographic verification.

---

## ⚡ Why FastAPI over Node.js for This Project

| Factor | FastAPI (Python) | Node.js/Fastify |
|---|---|---|
| **Auto API Docs** | ✅ Built-in Swagger + ReDoc | ❌ Requires manual setup |
| **Data Validation** | ✅ Pydantic v2 (runtime + type hints) | Requires Zod or Joi |
| **AI/ML Integration** | ✅ Native (LangChain, OpenAI, HuggingFace) | ❌ Awkward via HTTP calls |
| **Async Support** | ✅ First-class `async/await` | ✅ First-class |
| **Developer Speed** | ✅ Less boilerplate | Moderate |
| **Background Tasks** | Celery (battle-tested) | BullMQ (excellent) |
| **Ecosystem for Bots** | ✅ Rich (Tweepy, instagrapi, etc.) | Limited |

> **Bottom line:** FastAPI gives you the same async performance as Fastify, but with Python's superior ecosystem for social media libraries, AI personalization, and data processing — making it the ideal backbone for an Auto DM platform.
