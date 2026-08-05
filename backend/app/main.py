"""FastAPI app: CORS, router registration, healthcheck.

In production, schema changes are applied with `alembic upgrade head` on deploy —
not with create_all — so migrations stay the single source of truth.
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import settings
from app.routers import auth, jobs

app = FastAPI(title="Full-Stack-Job-Board API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(jobs.router)


@app.get("/health", tags=["meta"])
def health() -> dict:
    return {"status": "ok"}
