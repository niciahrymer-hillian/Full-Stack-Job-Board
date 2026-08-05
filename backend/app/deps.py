"""Auth dependency: turn a Bearer token into the current User, or 401.

Endpoints that require login just add `user: User = Depends(get_current_user)`.
Authorization (who may do what) lives in the routers/service layer, not here.
"""
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import User
from app.security import decode_token

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")


def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db),
) -> User:
    sub = decode_token(token)
    user = db.get(User, int(sub)) if sub and sub.isdigit() else None
    if user is None:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Invalid credentials")
    return user
