"""SQLAlchemy 2.0 ORM models — note the typed `Mapped[]` style.

The relationships model the domain: a User posts many Jobs; a User submits many
Applications; a Job receives many Applications. Cascade deletes keep orphans out.
"""
from datetime import datetime

from sqlalchemy import ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(unique=True, index=True)
    hashed_password: Mapped[str]
    is_employer: Mapped[bool] = mapped_column(default=False)

    jobs: Mapped[list["Job"]] = relationship(back_populates="owner", cascade="all, delete-orphan")
    applications: Mapped[list["Application"]] = relationship(back_populates="applicant", cascade="all, delete-orphan")


class Job(Base):
    __tablename__ = "jobs"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(index=True)
    description: Mapped[str]
    location: Mapped[str] = mapped_column(default="Remote")
    owner_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())

    owner: Mapped[User] = relationship(back_populates="jobs")
    applications: Mapped[list["Application"]] = relationship(back_populates="job", cascade="all, delete-orphan")


class Application(Base):
    __tablename__ = "applications"

    id: Mapped[int] = mapped_column(primary_key=True)
    job_id: Mapped[int] = mapped_column(ForeignKey("jobs.id"))
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    cover_letter: Mapped[str] = mapped_column(default="")

    job: Mapped[Job] = relationship(back_populates="applications")
    applicant: Mapped[User] = relationship(back_populates="applications")
