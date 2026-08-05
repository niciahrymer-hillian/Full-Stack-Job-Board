"""Pydantic v2 request/response models.

Separate Create (input) and Read (output) schemas: the client never sends an id
or created_at, and the API never echoes a password. `from_attributes=True` lets
a Read model be built straight from an ORM object.
"""
from datetime import datetime

from pydantic import BaseModel, ConfigDict, EmailStr


class UserCreate(BaseModel):
    email: EmailStr
    password: str
    is_employer: bool = False


class UserRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    email: EmailStr
    is_employer: bool


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


class JobCreate(BaseModel):
    title: str
    description: str
    location: str = "Remote"


class JobRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    title: str
    description: str
    location: str
    owner_id: int
    created_at: datetime
