"""Common API dependencies."""

from __future__ import annotations

from fastapi import Depends, HTTPException, Security, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.orm import Session

from ..core.config import get_settings
from ..database import get_db

settings = get_settings()
security_scheme = HTTPBearer(auto_error=False)


def require_token(credentials: HTTPAuthorizationCredentials = Security(security_scheme)) -> str:
    """Simple bearer-token authentication for demo environments."""

    if not credentials or not credentials.credentials:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Missing authorization token")

    token = credentials.credentials
    if token != settings.auth_token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid authorization token")

    return token


def get_db_session() -> Session:
    """Provide a SQLAlchemy session dependency."""

    yield from get_db()
