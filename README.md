# 💼 Full-Stack-Job-Board
### A FastAPI + React job board with JWT auth, deployed to Railway + Vercel.

![Chain C](https://img.shields.io/badge/Chain%20C-Project%201-378ADD?style=for-the-badge) [![License: AGPL v3](https://img.shields.io/badge/License-AGPLv3-blue?style=for-the-badge)](LICENSE-AGPL) [![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue?style=for-the-badge)](LICENSE-GPL)

[📖 Lesson Plan](docs/LESSON_PLAN.md) · [🎮 Interactive Tour](docs/interactive/index.html) · [🚀 Live Demo](#)

<!-- SCREENSHOT PLACEHOLDER: docs/screenshots/overview.png -->

## Why This Was Built

Almost every web product is the same shape underneath: a typed API, a token-based
auth boundary, a server-state cache on the client, and a database whose schema
changes over time. This project builds that shape end to end — a job board where
employers post roles and seekers apply — so the *pattern* is the deliverable, not
the domain. It's the reference I reach for when starting any new full-stack app.

## Tech Stack

| Technology | Version | Purpose |
|-----------|---------|---------|
| FastAPI | 0.115+ | Async API, dependency injection, auto OpenAPI docs |
| SQLAlchemy | 2.0 | ORM models + sessions (new typed style) |
| Alembic | 1.13+ | Versioned schema migrations |
| Pydantic | v2 | Request/response validation |
| python-jose | 3.3 | JWT encode/decode |
| passlib[bcrypt] | 1.7 | Password hashing |
| React | 18 | UI |
| React Query | v5 | Server-state cache (replaces useEffect data fetching) |
| Vite + TypeScript | 5 | Frontend build + type safety |
| PostgreSQL | 16 | Primary datastore |
| Railway / Vercel | — | API + frontend hosting |

## Project Structure

```
Full-Stack-Job-Board/
├── backend/
│   ├── app/
│   │   ├── main.py          ← FastAPI app + router registration
│   │   ├── config.py        ← settings from env
│   │   ├── database.py      ← engine, SessionLocal, get_db dependency
│   │   ├── models.py        ← SQLAlchemy 2.0 models (User, Job, Application)
│   │   ├── schemas.py       ← Pydantic v2 request/response models
│   │   ├── security.py      ← hashing + JWT helpers
│   │   ├── pagination.py    ← pure offset/limit helper (unit-tested)
│   │   ├── deps.py          ← get_current_user dependency
│   │   └── routers/{auth,jobs}.py
│   ├── tests/test_pagination.py
│   ├── requirements.txt
│   └── .env.example
├── frontend/
│   ├── src/{main.tsx, App.tsx, api/client.ts, hooks/useJobs.ts}
│   ├── package.json
│   └── .env.example
└── docs/{LESSON_PLAN.md, interactive/index.html, screenshots/}
```

## Getting Started

```bash
# Backend
cd backend
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env          # then fill DATABASE_URL + SECRET_KEY
alembic upgrade head
uvicorn app.main:app --reload  # docs at http://localhost:8000/docs

# Frontend
cd ../frontend
npm install
cp .env.example .env          # set VITE_API_URL=http://localhost:8000
npm run dev
```

## Chain Navigation

Part of **Chain C — Full-Stack + Infrastructure** in the [Post-Bootcamp-Challenge](https://github.com/niciahrymer-hillian/Post-Bootcamp-Challenge) portfolio. C-1 is the application; C-2 containerizes it, C-3 adds real-time ops, C-4 deploys on Kubernetes.

---

Dual licensed — [GPL v3](LICENSE-GPL) and [AGPL v3](LICENSE-AGPL).
