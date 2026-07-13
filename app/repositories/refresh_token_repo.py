from sqlalchemy.orm import Session

from app.models.refresh_tokens import RefreshToken


def create(
    db: Session,
    user_id: int,
    token: str,
    expires_at,
):
    refresh_token = RefreshToken(
        user_id=user_id,
        token=token,
        expires_at=expires_at,
    )

    db.add(refresh_token)
    db.commit()
    db.refresh(refresh_token)

    return refresh_token


def get_by_token(db: Session, token: str):
    return (
        db.query(RefreshToken)
        .filter(RefreshToken.token == token)
        .first()
    )


def revoke(db: Session, token: str):
    refresh_token = get_by_token(db, token)

    if not refresh_token:
        return None

    refresh_token.revoked = True

    db.commit()
    db.refresh(refresh_token)

    return refresh_token