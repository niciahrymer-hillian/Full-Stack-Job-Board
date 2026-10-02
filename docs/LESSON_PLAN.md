# 📖 Lesson Plan — Full-Stack-Job-Board

| Field | Value |
|-------|-------|
| Chain | Chain C — Full-Stack + Infrastructure (project C-1 of 4) |
| Difficulty | Intermediate |
| Estimated time | ~3 weeks |
| Prerequisite | Chain A/B fundamentals (Python, SQL, a little React) |
| Next project | [Dockerized-Microservices](../../Dockerized-Microservices) (C-2) |
| Primary license | AGPL v3 (deployed web app) |
| From scratch | No — skeleton scaffold (working bones + TODOs) |

## What This Project Is

A complete full-stack web application: a job board where employers post jobs and
seekers browse and apply. The point isn't the domain — it's wiring the four pieces
every modern web app shares: a typed REST API, a JWT auth boundary, a server-state
cache on the client, and a migrated relational schema.

You build the backend first (FastAPI + SQLAlchemy + Alembic + JWT), then the
frontend (React + Vite + React Query), then deploy each half to its natural host
(Railway for the API + Postgres, Vercel for the static frontend).

This is deliberately a **skeleton with working bones**: `app/security.py` and the
`/jobs` and `/auth` routers already run end-to-end — what's marked `# TODO` is the
extension work (typing `useCreateJob`'s input, adding the `/applications` list
view, wiring Alembic) that turns it into a showcase piece.

## Learning Objectives

- Build typed FastAPI routes with `Depends()`-based dependency injection for
  auth, database sessions, and authorization checks.
- Model a relational domain in SQLAlchemy 2.0's `Mapped[]` style, including
  cascading one-to-many relationships.
- Issue and verify JWTs, and explain precisely what "signed, not encrypted" means
  for what a token does and doesn't protect.
- Replace `useEffect` + `useState` data-fetching with React Query's cache,
  and trigger a refetch with `invalidateQueries` after a mutation.
- Generate, read, and reverse an Alembic migration, and explain why
  `--autogenerate` can't detect every kind of schema change.
- Deploy a split-repo full-stack app: stateless API on Railway, static SPA on
  Vercel, wired together by one environment variable.

## Software You Will Use

| Tool | What it is | Why it matters here | Install | Docs |
|------|-----------|----------------------|---------|------|
| FastAPI | Async Python web framework | Typed routes, automatic OpenAPI docs, `Depends()` DI | `pip install fastapi` | [FastAPI — Dependencies](https://fastapi.tiangolo.com/tutorial/dependencies/) |
| SQLAlchemy 2.0 | Python ORM / SQL toolkit | Typed `Mapped[]` models map directly to the `users`/`jobs`/`applications` tables | `pip install sqlalchemy` | [SQLAlchemy 2.0 — ORM Querying Guide](https://docs.sqlalchemy.org/en/20/orm/queryguide/index.html) |
| Alembic | SQLAlchemy's migration tool | Turns a model change into a versioned, reversible SQL script | `pip install alembic` | [Alembic — Auto Generating Migrations](https://alembic.sqlalchemy.org/en/latest/autogenerate.html) |
| python-jose + passlib | JWT encode/decode + bcrypt hashing | What `app/security.py` actually uses to sign tokens and hash passwords | `pip install "python-jose[cryptography]" "passlib[bcrypt]"` | [jwt.io — Introduction](https://jwt.io/introduction) |
| TanStack Query (React Query) v5 | Server-state cache for React | Replaces manual `useEffect` fetching with cache + invalidation | `npm install @tanstack/react-query` | [TanStack Query — Invalidation](https://tanstack.com/query/latest/docs/framework/react/guides/query-invalidation) |
| Vite | Frontend build tool | Fast dev server + TS/React template | `npm create vite@latest -- --template react-ts` | [Vite — Guide](https://vite.dev/guide/) |

## The Data Model

```
User (id, email, hashed_password, is_employer)
  ├─ 1:N → Job (id, title, description, location, owner_id, created_at)
  │          └─ 1:N → Application (id, job_id, user_id, cover_letter)
  └─ 1:N → Application  (the same table, from the applicant's side)
```

Both `Job` and `Application` cascade-delete from `User` (`cascade="all, delete-orphan"`
in `app/models.py`) — deleting a user never leaves an orphaned job posting or
application pointing at a user that no longer exists.

## The Interactive Tour

1. **The Full-Stack Architecture** — request lifecycle from browser → API → DB → back
2. **JWT Authentication** — hash → sign → verify, and what the signature does and doesn't protect
3. **React Query — Server State** — why it replaces `useEffect` + `useState` for data
4. **Database Migrations** — the anatomy of an Alembic migration, autogenerate's limits

## Build Order

- **Week 1 — Backend core.** `User`/`Job`/`Application` models + Pydantic schemas +
  `get_db` session dependency, then `/jobs` CRUD (`list_jobs`, `create_job`). Add
  Alembic (`alembic init alembic`), generate the first migration, run `upgrade head`.
  *Verify: `GET /jobs` returns `[]` against a fresh, migrated database.*
- **Week 2 — Auth + frontend.** JWT register/login in `app/routers/auth.py`, the
  `get_current_user` dependency, the employer-only check in `create_job`. Scaffold
  the React app (`npm create vite@latest`), wire `useJobs`/`useCreateJob` to `/jobs`.
  *Verify: posting a job as a non-employer returns `403`; as an employer, `201`.*
- **Week 3 — Apply flow + deploy.** `/jobs/{id}/apply` endpoint, protected routes on
  the client via `<ProtectedRoute>`, deploy the API to Railway (Postgres plugin +
  `alembic upgrade head` on release) and the frontend to Vercel (`VITE_API_URL`).
  *Verify: a deployed, logged-out visitor can browse jobs but is redirected to
  `/login` when they try to apply.*

## Common Mistakes to Avoid

- **Trusting the client to type the mutation body.** `useCreateJob`'s `# TODO` is
  there because an untyped `mutationFn` argument will happily send a wrong shape
  and fail only at the server — type it against a shared `JobCreate` interface.
- **Checking authorization in the wrong layer.** `create_job` raises `403` for a
  non-employer *inside the route*, after `get_current_user` has already
  authenticated them. Authentication (who are you) and authorization (are you
  allowed) are separate checks — conflating them is how a logged-in-but-wrong-role
  user slips through.
- **Hand-editing the schema instead of migrating it.** Changing a column directly
  in `psql` works until the next environment (staging, a teammate's machine, CI)
  doesn't have that change — Alembic's whole point is that every environment
  converges by replaying the same versioned steps.
- **Forgetting `invalidateQueries` after a mutation.** Without it, `useCreateJob`
  succeeds but the job list on screen is stale until a manual refresh — the
  mutation and the query are two separate caches until you connect them.

## Why This Matters (Industry Application)

**What this skill is used for in the real world**
This exact stack — a typed REST API, JWT-based auth, a relational schema under
migration control, and a server-state cache on the client — is the default shape
of production web applications at almost every company that isn't a monolith
shop. Job boards, internal admin tools, and SaaS dashboards are all the same
four pieces wired together differently.

**Roles that hire for it**
- Full-Stack Engineer · Backend Engineer (Python/FastAPI) · Frontend Engineer (React)
- Platform/Product Engineer at any company running a Python API + React frontend

**Why it strengthens *my* portfolio**
This is the foundational full-stack pattern that the rest of Chain C builds on
directly: C-2 containerizes this exact app, C-3 adds a real-time layer to a
sibling app, and C-4 deploys that containerized app to Kubernetes. It's also the
same JWT + SQLAlchemy + React Query pattern used throughout Centric/Entrada, so
the skill transfers straight into the real-estate product work.

**How it connects to the rest of the portfolio**
- Builds on: Chain A/B fundamentals (Python, SQL, React basics)
- Feeds into: [Chain C-2 — Dockerized-Microservices](../../Dockerized-Microservices), [Chain C-3 — Ops-Management-Dashboard](../../Ops-Management-Dashboard), [Chain C-4 — Kubernetes-IaC-Deployment](../../Kubernetes-IaC-Deployment)

## Reflection Questions

1. Why does React Query make `useEffect`-based fetching an anti-pattern for server data?
2. What exactly is inside a JWT, and why is it safe to send the signature but never the secret?
3. Why generate migrations with `--autogenerate` instead of editing the schema by hand in production — and what kinds of changes can't it detect on its own?
4. Where should authorization (not authentication) live — the router, the dependency, or the service layer? Why, and what does this project actually do?
5. What breaks if the frontend and API are on different domains, and how does CORS fix it?
6. If `SECRET_KEY` leaked, what could an attacker do with it — and what couldn't they do without also compromising the database?

## Topics to Research

- [FastAPI — OAuth2 with Password (and hashing), Bearer with JWT tokens](https://fastapi.tiangolo.com/tutorial/security/oauth2-jwt/)
- [SQLAlchemy 2.0 — ORM Querying Guide](https://docs.sqlalchemy.org/en/20/orm/queryguide/index.html)
- [Alembic — Auto Generating Migrations](https://alembic.sqlalchemy.org/en/latest/autogenerate.html)
- [TanStack Query — Important Defaults](https://tanstack.com/query/latest/docs/framework/react/guides/important-defaults)
- [jwt.io — Introduction](https://jwt.io/introduction)
- [MDN — Cross-Origin Resource Sharing (CORS)](https://developer.mozilla.org/en-US/docs/Web/HTTP/Guides/CORS)

## How This Connects Forward

This app is the thing **C-2** containerizes, **C-3** extends with real-time ops
dashboards, and **C-4** deploys on Kubernetes. Keep the API stateless so those
later chains can scale it horizontally.

## Git Commit Checklist

- [ ] Conventional commits, one feature each (`feat:`, `fix:`, `chore:`).
- [ ] Backend and frontend changes in separate commits.
- [ ] Never commit `.env` or build artifacts.
