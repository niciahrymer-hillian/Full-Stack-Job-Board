# 📖 Lesson Plan — Full-Stack-Job-Board

| Field | Value |
|-------|-------|
| Chain | Chain C — Full-Stack + Infrastructure |
| Difficulty | Intermediate |
| Duration | ~3 weeks |
| Prerequisite | Chain A/B fundamentals (Python, SQL, a little React) |

## What This Project Is

A complete full-stack web application: a job board where employers post jobs and
seekers browse and apply. The point isn't the domain — it's wiring the four pieces
every modern web app shares: a typed REST API, a JWT auth boundary, a server-state
cache on the client, and a migrated relational schema.

You build the backend first (FastAPI + SQLAlchemy + Alembic + JWT), then the
frontend (React + Vite + React Query), then deploy each half to its natural host
(Railway for the API + Postgres, Vercel for the static frontend).

## Topics Covered

**Backend**
- FastAPI route handlers, `Depends()` for DI, async vs sync endpoints
- Pydantic v2 schemas: `model_config`, `from_attributes`, separate Create/Read models
- SQLAlchemy 2.0 ORM: `Mapped[]` typed models, relationships, sessions
- Alembic migrations: `revision --autogenerate`, `upgrade head`, `downgrade`
- JWT auth: `passlib[bcrypt]` hashing, `python-jose` tokens, `OAuth2PasswordBearer`

**Frontend**
- React Query v5: `useQuery`, `useMutation`, cache invalidation with `invalidateQueries`
- Vite + TypeScript: `npm create vite@latest -- --template react-ts`
- Protected routes via a `<ProtectedRoute>` wrapper + React Router
- Axios interceptor that attaches the JWT to every request

**Deployment**
- Railway: env vars, attaching the PostgreSQL plugin, running migrations on deploy
- Vercel: `VITE_API_URL` env var, SPA rewrites

## The Interactive Tour

1. **The Full-Stack Architecture** — request lifecycle from browser → API → DB → back
2. **JWT Authentication** — register → hash → token → protected route, animated
3. **React Query: Server State** — why it beats `useEffect` + `useState` for data
4. **Database Migrations** — the anatomy of an Alembic migration file

## Build Order

- **Week 1 — Backend core.** Models + schemas + database session, then `/jobs` CRUD. Add Alembic and generate the first migration.
- **Week 2 — Auth + frontend.** JWT register/login, `get_current_user` dependency, protected create-job route. Scaffold the React app, wire React Query to `/jobs`.
- **Week 3 — Apply flow + deploy.** Application model + endpoint, protected routes on the client, deploy API to Railway and frontend to Vercel.

## Reflection Questions

1. Why does React Query make `useEffect`-based fetching an anti-pattern for server data?
2. What exactly is inside a JWT, and why is it safe to send the signature but never the secret?
3. Why generate migrations with `--autogenerate` instead of editing the schema by hand in production?
4. Where should authorization (not authentication) live — the router, the dependency, or the service layer? Why?
5. What breaks if the frontend and API are on different domains, and how does CORS fix it?

## How This Connects Forward

This app is the thing **C-2** containerizes, **C-3** extends with real-time ops
dashboards, and **C-4** deploys on Kubernetes. Keep the API stateless so those
later chains can scale it horizontally.

## Git Commit Checklist

- [ ] Conventional commits, one feature each (`feat:`, `fix:`, `chore:`).
- [ ] Backend and frontend changes in separate commits.
- [ ] Never commit `.env` or build artifacts.
