"""Password hashing + JWT helpers.

Passwords are hashed with bcrypt (slow by design) and never stored in plaintext.
JWTs are *signed* with SECRET_KEY (HS256), not encrypted — anyone can read the
claims, but only the server can forge a valid signature.
"""
from datetime import datetime, timedelta, timezone

from jose import jwt
from passlib.context import CryptContext

from app.config import settings

_pwd = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(plain: str) -> str:
    return _pwd.hash(plain)


def verify_password(plain: str, hashed: str) -> bool:
    return _pwd.verify(plain, hashed)


def create_access_token(subject: str) -> str:
    expire = datetime.now(timezone.utc) + timedelta(hours=settings.access_token_expire_hours)
    payload = {"sub": subject, "exp": expire}
    return jwt.encode(payload, settings.secret_key, algorithm="HS256")


def decode_token(token: str) -> str | None:
    """Return the subject claim, or None if the token is invalid/expired."""
    try:
        return jwt.decode(token, settings.secret_key, algorithms=["HS256"]).get("sub")
    except jwt.JWTError:
        return None
