"""Job listing + posting + applying.

Listing is public; posting requires an employer; applying requires any logged-in
user. Note where authorization lives: in the endpoint, after authentication.
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.database import get_db
from app.deps import get_current_user
from app.models import Application, Job, User
from app.pagination import paginate
from app.schemas import JobCreate, JobRead

router = APIRouter(prefix="/jobs", tags=["jobs"])


@router.get("", response_model=list[JobRead])
def list_jobs(page: int = 1, size: int = 20, db: Session = Depends(get_db)) -> list[Job]:
    offset, limit = paginate(page, size)
    return list(db.scalars(select(Job).order_by(Job.created_at.desc()).offset(offset).limit(limit)))


@router.post("", response_model=JobRead, status_code=201)
def create_job(
    payload: JobCreate,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
) -> Job:
    if not user.is_employer:
        raise HTTPException(status.HTTP_403_FORBIDDEN, "Only employers can post jobs")
    job = Job(**payload.model_dump(), owner_id=user.id)
    db.add(job)
    db.commit()
    db.refresh(job)
    return job


@router.post("/{job_id}/apply", status_code=201)
def apply(
    job_id: int,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
) -> dict:
    if not db.get(Job, job_id):
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Job not found")
    db.add(Application(job_id=job_id, user_id=user.id))
    db.commit()
    return {"status": "applied", "job_id": job_id}
