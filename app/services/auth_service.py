from sqlalchemy.orm import Session

from app.core.security import (
    create_access_token,
    create_refresh_token,
    decode_token,
    hash_password,
    verify_password,
)
from app.repositories import (
    refresh_token_repo,
    user_repo,
)


def register_user(
    db: Session,
    name: str,
    password: str,
):
    hashed_password = hash_password(password)

    return user_repo.create(
        db,
        name,
        hashed_password,
    )


def login_user(
    db: Session,
    name: str,
    password: str,
):
    user = user_repo.get_by_name(
        db,
        name,
    )

    if not user:
        return None

    if not verify_password(
        password,
        user.hashed_password,
    ):
        return None

    access_token = create_access_token(
        {"user_id": user.id}
    )

    refresh_token, expires = create_refresh_token(
        {"user_id": user.id}
    )

    refresh_token_repo.create(
        db,
        user.id,
        refresh_token,
        expires,
    )

    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
    }


def refresh_access_token(
    db: Session,
    refresh_token: str,
):
    stored_token = refresh_token_repo.get_by_token(
        db,
        refresh_token,
    )

    if not stored_token:
        return None

    if stored_token.revoked:
        return None

    payload = decode_token(refresh_token)

    if not payload:
        return None

    if payload.get("type") != "refresh":
        return None

    user_id = payload.get("user_id")

    if not user_id:
        return None

    return create_access_token(
        {"user_id": user_id}
    )


def logout_user(
    db: Session,
    refresh_token: str,
):
    return refresh_token_repo.revoke(
        db,
        refresh_token,
    )