from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.security import (
    HTTPAuthorizationCredentials,
    decode_token,
    oauth2_schema,
)
from app.dependencies.db import get_db
from app.repositories import user_repo


def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(oauth2_schema),
    db: Session = Depends(get_db),
):
    token = credentials.credentials

    payload = decode_token(token)

    if not payload:
        return None

    user_id = payload.get("user_id")

    if not user_id:
        return None

    return user_repo.get_by_id(db, user_id)


def require_admin(user=Depends(get_current_user)):
    if not user:
        return None

    if user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions",
        )

    return user